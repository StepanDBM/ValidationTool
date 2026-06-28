from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_SCENE_READY_FOR_EXPORT

def check_scene_ready_for_export(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_meshes == 0 or obj.total_cameras == 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_SCENE_READY_FOR_EXPORT,
            severity=ValidationSeverity.ERROR,
            message="Scene is not ready for export.",
            suggestion="Ensure meshes and cameras exist."
        )
