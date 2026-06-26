import datetime
import copy
import uuid
import json
from collections import Counter
from typing import List
import reporting.staged_json_reporter as json_reporter
from pathlib import Path

import core.validation_models as valMod
from core.registry import ValidationRegistry
from core.validation_system import FixMode

from core.ProfileManagement.AttributeOverride import apply_overrides
from core.ProfileManagement.ProfileModels import ProfileConfig

from core.context.baseContext import BaseContext
from core.context import baseContext, mesh_context, camera_context, light_context


import core.checks.Naming.check_default_dcc_name as Check_DefDCCName
import core.checks.Naming.check_double_underscore as Check_DublUnderscore
import core.checks.Naming.check_invalid_characters as Check_InvChars
import core.checks.Naming.check_name_pattern as Check_NamePattern
import core.checks.Naming.check_valid_prefix as Check_ValPrefix

import core.checks.Transform.check_zero_scale as Check_0Scl
import core.checks.Transform.check_non_uniform_scale as Check_NonUniScl
import core.checks.Transform.check_negative_scale as Check_NegScl
import core.checks.Transform.check_extreme_scale as Check_XtrmScl

import core.checks.Geometry.check_vertex_count as Check_VtxCount
import core.checks.Geometry.check_triangle_count as Check_TrisCount
#import core.checks.Geometry.check_collision_readiness as Check_CollisionReady
#import core.checks.Geometry.check_bounding_box as Check_BoundBox
#import core.checks.Geometry.check_degenerate_faces as Check_DegenFaces
import core.checks.Geometry.check_hard_edges as Check_HardEdges
#import core.checks.Geometry.check_hidden_geometry as Check_HiddenGeo
import core.checks.Geometry.check_isolated_vertices as Check_IsolVtx
import core.checks.Geometry.check_lamina_faces as Check_LaminaFaces
import core.checks.Geometry.check_ngons as Check_NGons
#import core.checks.Geometry.check_non_manifold as Check_NonManifold
import core.checks.Geometry.check_normals_exist as Check_NormalsExist
import core.checks.Geometry.check_normals as Check_Normals
import core.checks.Geometry.check_overlapping_geometry as Check_OverlapGeo

import core.checks.Uv.check_empty_uv_set_names as Check_EmptUVSetNames
import core.checks.Uv.check_duplicate_uv_set_names as Check_DuplUVSetNames
import core.checks.Uv.check_missing_uv as Check_MissingUV

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
    registry.register(Check_VtxCount.check_vertex_count,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_TrisCount.check_triangle_count,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_HardEdges.check_hard_edges,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_IsolVtx.check_isolated_vertices,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_LaminaFaces.check_lamina_faces,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_NGons.check_ngons,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_NormalsExist.check_normals_exist,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_Normals.check_broken_normals,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)
    registry.register(Check_OverlapGeo.check_overlapping_geo,
                      target_types=[mesh_context.MeshContext],
                      category=GEOMETRY, stage=excS.GEOMETRY)


    registry.register(Check_EmptUVSetNames.check_empty_uv_set_names,
                      target_types=[mesh_context.MeshContext],
                      category=UV, stage=excS.UV)
    registry.register(Check_DuplUVSetNames.check_duplicate_uv_set_names,
                      target_types=[mesh_context.MeshContext],
                      category=UV, stage=excS.UV)
    registry.register(Check_MissingUV.check_missing_uvs,
                      target_types=[mesh_context.MeshContext],
                      category=UV, stage=excS.UV)
    
    
    registry.register(Check_0Scl.check_null_scale,
                      target_types=[mesh_context.MeshContext, camera_context.CameraContext, light_context.LightContext],
                      category=TRANSFORM, stage=excS.TRANSFORM)
    registry.register(Check_NonUniScl.check_nonUni_scale,
                      target_types=[mesh_context.MeshContext, camera_context.CameraContext, light_context.LightContext],
                      category=TRANSFORM, stage=excS.TRANSFORM)
    registry.register(Check_NegScl.check_negative_scale,
                      target_types=[mesh_context.MeshContext, camera_context.CameraContext, light_context.LightContext],
                      category=TRANSFORM, stage=excS.TRANSFORM)
    registry.register(Check_XtrmScl.check_extreme_scale,
                      target_types=[mesh_context.MeshContext, camera_context.CameraContext, light_context.LightContext],
                      category=TRANSFORM, stage=excS.TRANSFORM, fix_mode=FixMode.SEMI)
    
    
    registry.register(Check_DefDCCName.check_default_dcc_naming,
                      target_types=[baseContext.BaseContext],
                      category=NAMING, stage=excS.NAMING)
    registry.register(Check_DublUnderscore.check_double_underscore,
                      target_types=[baseContext.BaseContext],
                      category=NAMING, stage=excS.NAMING ,fix_mode=FixMode.AUTO)
    registry.register(Check_InvChars.check_invalid_characters,
                      target_types=[baseContext.BaseContext],
                      category=NAMING, stage=excS.NAMING)
    registry.register(Check_NamePattern.check_name_pattern,
                      target_types=[baseContext.BaseContext],
                      category=NAMING, stage=excS.NAMING)
    registry.register(Check_ValPrefix.check_valid_prefix,
                      target_types=[baseContext.BaseContext],
                      category=NAMING, stage=excS.NAMING)
    
    return registry

def run_pipeline(objects: List[BaseContext], context, profile:ProfileConfig=None):
    loader = ConfigLoader(absPath.CONFIG_DIR)
    validation_config = loader.load_validation_config()
    naming_rules = loader.load_naming_rules()
    budgets = loader.load_budgets()

    effective_config = valCtx.ValidationRuntimeContext(
        validation=copy.deepcopy(validation_config),
        naming=copy.deepcopy(naming_rules),
        budgets=copy.deepcopy(budgets)
    )

    if profile is not None and getattr(profile, "overrides", None):
        apply_overrides(effective_config, profile.overrides)

    runtime_ctx = valCtx.ValidationRuntimeContext(
        validation=effective_config.validation,
        naming=effective_config.naming,
        budgets=effective_config.budgets
    )

    registry = build_registry()
    run_id = str(uuid.uuid4().hex[:8])
    timestamp = datetime.datetime.now().isoformat()
    this_artist = Path.home() / "Documents/ValidationTool/Artists/StepanBatlloriMartinez/artistLog.json"
    if(context.get("headless") == 1):
        with open(absPath.ARTISTS_DIR / context.get("artist"),
                "r", encoding="utf-8") as f:
            this_artist = json.load(f)
    else:
        with open(this_artist,
                "r", encoding="utf-8") as f:
            this_artist = json.load(f)
    all_results_flat = []
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

            all_results_flat.append(result)
            new_issue = valMod.ValidationResult(
                artist=this_artist,
                dcc=context.get("dcc"),
                origin_file=context.get("path"),
                object_name=obj.name,
                check_name=result.check_name,
                stage=check.stage,
                timestamp=timestamp,
                severity=result.severity,
                message=result.message,
                suggestion=result.suggestion,
                fix_mode=check.fix_mode
            )
            #Here the AUTOfixed Checks should be resolved and send a resolution Issue, not an "error" resolution.
            all_issues.append(new_issue)

            if result.severity == valMod.ValidationSeverity.HARD:
                hard_stop = True

            if hard_stop:
                break

    counts = Counter(i.severity.value for i in all_results_flat)

    summary = valMod.RunSummary(
        run_id=run_id,
        timestamp=timestamp,
        dcc=context.get("dcc"),
        total_objects=len(objects),
        total_issues=len(all_results_flat),
        errors=counts.get("ERROR", 0),
        warnings=counts.get("WARNING", 0),
        infos=counts.get("INFO", 0)
    )

    run = valMod.ValidationRun(
        summary=summary,
        scene_setup=context.get("scene_setup"),
        issues=all_issues,
        jsonPath=""
    )

    new_json_path = json_reporter.write_json(run, pretty=True)
    run.jsonPath = new_json_path
    return run
