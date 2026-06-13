import datetime
import uuid
import json
from collections import Counter
from typing import List
import reporting.staged_json_reporter as json_reporter

import core.validation_models as valMod
from core.registry import ValidationRegistry

from core.context.baseContext import BaseContext
from core.context import baseContext, mesh_context

import core.checks.check_transforms as check_transforms
import core.checks.check_naming as check_naming
import core.checks.check_mesh as check_mesh
import core.checks.check_uv as check_uv

import config.absolutePaths as absPath
from config.check_categories import (
    GEOMETRY,
    UV,
    TRANSFORM,
    NAMING
)

import config.exec_stages as excS

import core.validation_context as valCtx

from reporting.config_loader import ConfigLoader


def build_registry() -> ValidationRegistry:

    registry = ValidationRegistry()
    registry.register(check_mesh.check_vertex_count,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(check_mesh.check_triangle_count,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)

    #registry.register(check_material_slots)
    registry.register(check_uv.check_uv_sets,
                      target_types=[mesh_context.MeshContext],
                      category=UV, stage=excS.UV)
    #registry.register(check_non_manifold)
    #registry.register(check_degenerate_faces)
    
    registry.register(check_transforms.check_transforms,
                      target_types=[mesh_context.MeshContext],#could add CameraContext, SkeletonContext...
                      category=TRANSFORM, stage=excS.TRANSFORM)
    registry.register(check_naming.check_naming,
                      target_types=[baseContext.BaseContext], #everything should have correct naming
                      category=NAMING, stage=excS.NAMING)
    #registry.register(check_bounding_box)

    return registry

def print_report2(issues: List[valMod.ValidationResult]):

    print("\n--- ValidationResult LIST REPORT ---\n")

    for issue in issues:
        print(
            f"[{issue.dcc}] "
            f"{issue.asset_name} | "
            f"{issue.check_name} -> "
            f"{issue.stage}."
            f"{issue.timestamp}"
            f"{issue.severity}"
            f"{issue.message}"
            f"{issue.suggestion}"
        )



def run_pipeline(objects: List[BaseContext], context, profile=None):
    loader = ConfigLoader(absPath.ROOT_PATH)

    validation_config = loader.load_validation_config()
    naming_rules = loader.load_naming_rules()
    budgets = loader.load_budgets()

    runtime_ctx = valCtx.ValidationRuntimeContext(
        validation_config=validation_config,
        naming_rules=naming_rules,
        budgets=budgets
    )

    registry = build_registry()
    run_id = str(uuid.uuid4().hex[:8])
    timestamp = datetime.datetime.now().isoformat()

    with open(context.get("artist"), "r", encoding="utf-8") as f:
        this_artist = json.load(f)

    all_issues_flat = []
    all_issues = []

    ordered_checks = registry.resolveByProfileStage(profile)

    for obj in objects:
        hard_stop = False

        for check in ordered_checks:
            # Skip checks that do not apply to this context type
            
            if not isinstance(obj, tuple(check.target_types)):
                    continue

            result = check.func(obj, runtime_ctx)
            if not result:
                continue


            all_issues_flat.extend(result)

            for issue in result:
                new_issue = valMod.ValidationResult(
                    artist=this_artist,
                    dcc=context.get("dcc"),
                    origin_file=context.get("path"),
                    object_name=obj.name,
                    check_name=issue.check_name,
                    stage=check.stage,
                    timestamp=timestamp,
                    severity=issue.severity,
                    message=issue.message,
                    suggestion=issue.suggestion
                )
                all_issues.append(new_issue)

                if issue.severity == valMod.ValidationSeverity.HARD:
                    hard_stop = True

            if hard_stop:
                break

    counts = Counter(i.severity.value for i in all_issues_flat)

    summary = valMod.RunSummary(
        run_id=run_id,
        timestamp=timestamp,
        dcc=context.get("dcc"),
        total_objects=len(objects),
        total_issues=len(all_issues_flat),
        errors=counts.get("ERROR", 0),
        warnings=counts.get("WARNING", 0),
        infos=counts.get("INFO", 0)
    )

    run = valMod.ValidationRun(
        summary=summary,
        issues=all_issues,
        jsonPath=""
    )

    new_json_path = json_reporter.write_json(run, absPath.REPORTS_DIR, pretty=True)
    run.jsonPath = new_json_path
    return run
