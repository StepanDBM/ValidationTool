import datetime
import time
import uuid
from collections import Counter
from typing import List, Optional
import reporting.staged_json_reporter as json_reporter

from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)
from config.validation_config import ValidationConfig

from core.registry import MeshValidatorRegistry

import checks.check_mesh as check_mesh

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


def run_validation(meshes, registry, profile):

    all_issues = []

    checks_by_stage = registry.resolveByProfileStage(profile)

    for mesh in meshes:

        for stage in excS.EXECUTION_STAGES:

            stage_checks = [
                c for c in checks_by_stage
                if c.stage == stage
            ]

            stage_issues = []

            for check in stage_checks:
                stage_issues.extend(check.func(mesh))

            all_issues.extend(stage_issues)

            # STAGE GATE
            if any(i.severity.value == "ERROR" for i in stage_issues):
                print(f"[PIPELINE STOP] {stage} failed on {mesh.name}")
                break

    return all_issues


def evaluate_results(
    issues: List[ValidationIssue],
    config: ValidationConfig
) -> bool:

    errors = [
        issue
        for issue in issues
        if issue.severity == ValidationSeverity.ERROR
    ]

    if config.strict_mode and errors:
        return False

    return True


def print_report(issues: List[ValidationIssue]):

    print("\n--- VALIDATION REPORT ---\n")

    for issue in issues:
        print(
            f"[{issue.severity.value}] "
            f"{issue.asset_name} | "
            f"{issue.check_name} -> "
            f"{issue.message}"
        )


def run_pipeline(meshes, config, profile=None):

    registry = build_registry()
    run_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now()

    asset_results = []
    all_issues_flat = []

    for mesh in meshes:

        stage_results = []

        asset_has_errors = False
        asset_issue_count = 0

        ordered_checks = registry.resolveByProfileStage(profile)

        current_stage = None
        stage_issues = []
        stage_start_time = time.time()

        for check in ordered_checks:

            # detect stage change
            if current_stage is None:
                current_stage = check.stage

            if check.stage != current_stage:

                # flush previous stage
                stage_results.append(
                    valMod.StageResult(
                        stage=current_stage,
                        issues=stage_issues,
                        has_errors=any(i.severity.value == "ERROR" for i in stage_issues),
                        execution_time=time.time() - stage_start_time
                    )
                )

                # reset stage
                current_stage = check.stage
                stage_issues = []
                stage_start_time = time.time()

            # execute check
            result = check.func(mesh)

            stage_issues.extend(result)
            all_issues_flat.extend(result)
            
            asset_issue_count += len(result)

            if any(i.severity.value == "ERROR" for i in result):
                asset_has_errors = True

        # flush last stage
        if current_stage is not None:
            stage_results.append(
                valMod.StageResult(
                    stage=current_stage,
                    issues=stage_issues,
                    has_errors=any(i.severity.value == "ERROR" for i in stage_issues),
                    execution_time=time.time() - stage_start_time
                )
            )

        asset_results.append(
            valMod.AssetValidationResult(
                asset_name=mesh.name,
                stages=stage_results,
                total_issues=asset_issue_count,
                has_errors=asset_has_errors
            )
        )

    counts = Counter(i.severity.value for i in all_issues_flat)

    summary = valMod.PipelineSummary(
        total_assets=len(meshes),
        total_issues=len(all_issues_flat),
        errors=counts.get("ERROR", 0),
        warnings=counts.get("WARNING", 0),
        infos=counts.get("INFO", 0)
    )
    
    run = valMod.ValidationRun(
        run_id=run_id,
        timestamp=timestamp,
        assets=asset_results,
        summary=summary
    )
    json_reporter.write_json(run, r"E:\Work\3D\my_3D\PIPELINE\reports", pretty=True)
    return run