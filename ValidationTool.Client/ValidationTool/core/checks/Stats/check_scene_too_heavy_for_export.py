from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_SCENE_TOO_HEAVY_FOR_EXPORT

def check_scene_too_heavy_for_export(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    score = obj.total_meshes + obj.total_transforms + obj.total_references

    if score > 10000:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_SCENE_TOO_HEAVY_FOR_EXPORT,
            severity=ValidationSeverity.ERROR,
            message=f"Scene too heavy ({score}).",
            suggestion="Reduce geometry or references."
        )
