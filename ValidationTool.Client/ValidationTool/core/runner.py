import datetime
import uuid
from collections import Counter
from typing import List
import reporting.staged_json_reporter as json_reporter

from core.validation_system import (
    ValidationIssue
)

from core.registry import MeshValidatorRegistry

import checks.check_mesh as check_mesh

import config.absolutePaths as absPath
from config.check_categories import (
    GEOMETRY,
    UV,
    TRANSFORM,
    NAMING
)

import checks.check_naming as check_naming
import checks.check_uv as check_uv

import checks.check_transforms as check_transforms

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

def print_report(issues: List[ValidationIssue]):

    print("\n--- VALIDATION REPORT ---\n")

    for issue in issues:
        print(
            f"[{issue.severity.value}] "
            f"{issue.asset_name} | "
            f"{issue.check_name} -> "
            f"{issue.message}"
        )


def run_pipeline(mObjects: valSys.MeshContext, context, profile=None):
    
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
    run_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now()

    all_issues_flat = []

    for mObject in mObjects:
        print(f"Curent mObject: {mObject.name}", flush=True)

        asset_issue_count = 0

        ordered_checks = registry.resolveByProfileStage(profile)
        allIssues = []

        for check in ordered_checks:
            result = check.func(mObject, runtime_ctx)

            all_issues_flat.extend(result)
            
            asset_issue_count += len(result)
            thispos = len(all_issues_flat)-1
            newIssue = AssetValidationResult(
                dcc = context.get("dcc"),
                asset_name = mObject.name,
                check_name = all_issues_flat[thispos].check_name,
                stage = check.stage,
                timestamp = datetime.datetime.now(),
                severity = all_issues_flat[thispos].severity,
                message = all_issues_flat[thispos].message,
                suggestion = all_issues_flat[thispos].suggestion
            )

            allIssues.append(newIssue)

    counts = Counter(i.severity.value for i in all_issues_flat)

    summary = valMod.RunSummary(
        run_id = run_id,
        timestamp = timestamp,
        dcc = context.get("dcc"),
        total_assets = len(mObjects),
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