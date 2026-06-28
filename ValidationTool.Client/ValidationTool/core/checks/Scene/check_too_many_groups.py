from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_GROUPS

def check_too_many_groups(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    limit = getattr(runtime_ctx.validation, "max_groups", 50)

    if len(obj.groups) > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_GROUPS,
            severity=ValidationSeverity.WARNING,
            message=f"Too many group nodes: {len(obj.groups)}",
            suggestion="Simplify scene hierarchy."
        )