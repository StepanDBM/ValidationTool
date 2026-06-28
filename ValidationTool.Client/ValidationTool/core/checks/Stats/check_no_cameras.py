from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_NO_CAMERAS

def check_no_cameras(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_cameras == 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_NO_CAMERAS,
            severity=ValidationSeverity.ERROR,
            message="No cameras in scene.",
            suggestion="Add render camera."
        )