from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_CAMERAS

def check_too_many_cameras(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_cameras > 10:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_CAMERAS,
            severity=ValidationSeverity.WARNING,
            message=f"Too many cameras: {obj.total_cameras}",
            suggestion="Keep only required cameras."
        )