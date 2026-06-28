from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_NO_LIGHTS

def check_no_lights(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_lights == 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_NO_LIGHTS,
            severity=ValidationSeverity.WARNING,
            message="No lights in scene.",
            suggestion="Add basic lighting."
        )