from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_LIGHTS

def check_too_many_lights(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_lights > 50:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_LIGHTS,
            severity=ValidationSeverity.WARNING,
            message=f"Too many lights: {obj.total_lights}",
            suggestion="Reduce lighting complexity."
        )