from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_CAMERA_TO_OBJECT_RATIO

def check_camera_to_object_ratio(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_meshes > 0 and obj.total_cameras / obj.total_meshes > 0.5:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_CAMERA_TO_OBJECT_RATIO,
            severity=ValidationSeverity.INFO,
            message="Too many cameras relative to objects.",
            suggestion="Reduce unnecessary cameras."
        )
