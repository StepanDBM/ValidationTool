import datetime
import uuid
import json
from collections import Counter
from typing import List
import reporting.staged_json_reporter as json_reporter


from core.registry import MeshValidatorRegistry

import core.checks.check_mesh as check_mesh

import config.absolutePaths as absPath
from config.check_categories import (
    GEOMETRY,
    UV,
    TRANSFORM,
    NAMING
)

import core.checks.check_naming as check_naming
import core.checks.check_uv as check_uv

import core.checks.check_transforms as check_transforms

import config.exec_stages as excS

import core.validation_models as valMod
from core.validation_models import AssetValidationResult
import core.validation_system as valSys
import core.validation_context as valCtx

from reporting.config_loader import ConfigLoader


def build_registry() -> MeshValidatorRegistry:

    registry = MeshValidatorRegistry()
    registry.register(check_mesh.check_vertex_count, category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(check_mesh.check_triangle_count, category=GEOMETRY, stage=excS.GEOMETRY)

    #registry.register(check_material_slots)
    registry.register(check_uv.check_uv_sets, category=UV, stage=excS.UV)
    #registry.register(check_non_manifold)
    #registry.register(check_degenerate_faces)
    
    registry.register(check_transforms.check_transforms, category=TRANSFORM, stage=excS.TRANSFORM)
    registry.register(check_naming.check_naming, category=NAMING, stage=excS.NAMING)
    #registry.register(check_bounding_box)

    return registry

def print_report2(issues: List[AssetValidationResult]):

    print("\n--- AssetValidationResult LIST REPORT ---\n")

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


def run_pipeline(mObjects: valSys.ObjectContext, context, profile=None):
    
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
        thisArtist = json.load(f)

    all_issues_flat = []
    allIssues = []
    for mObject in mObjects:

        ordered_checks = registry.resolveByProfileStage(profile)

        for check in ordered_checks:
            result = check.func(mObject, runtime_ctx)

            all_issues_flat.extend(result)
            for issue in result:
                newIssue = AssetValidationResult(
                    artist = thisArtist,
                    dcc = context.get("dcc"),
                    originFile=context.get("path"),
                    asset_name = mObject.name,
                    check_name = issue.check_name,
                    stage = check.stage,
                    timestamp = timestamp,
                    severity = issue.severity,
                    message = issue.message,
                    suggestion = issue.suggestion
                )
                allIssues.append(newIssue)

    counts = Counter(i.severity.value for i in all_issues_flat)
    summary = valMod.RunSummary(
        run_id = run_id,
        timestamp = timestamp,
        dcc = context.get("dcc"),
        total_objects = len(mObjects),
        total_issues = len(all_issues_flat),
        errors = counts.get("ERROR", 0),
        warnings = counts.get("WARNING", 0),
        infos = counts.get("INFO", 0)
    )
    
    
    run = valMod.ValidationRun(
        summary = summary,
        issues = allIssues,
        jsonPath = ""
    )

    newJsonPath = json_reporter.write_json(run, absPath.REPORTS_DIR, pretty=True)
    run.jsonPath = newJsonPath
    return run