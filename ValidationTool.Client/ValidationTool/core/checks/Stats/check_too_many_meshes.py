from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_MESHES

def check_too_many_meshes(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    limit = getattr(runtime_ctx.budgets, "max_meshes", 500)

    if obj.total_meshes > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_MESHES,
            severity=ValidationSeverity.WARNING,
            message=f"Too many meshes: {obj.total_meshes}",
            suggestion="Optimize geometry."
        )
