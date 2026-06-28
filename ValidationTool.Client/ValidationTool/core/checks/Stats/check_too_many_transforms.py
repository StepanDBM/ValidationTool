from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_TRANSFORMS

def check_too_many_transforms(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    if obj.total_transforms > 5000:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_TRANSFORMS,
            severity=ValidationSeverity.WARNING,
            message=f"Too many transforms: {obj.total_transforms}",
            suggestion="Simplify hierarchy."
        )