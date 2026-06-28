from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_HIERARCHY_DEPTH_TOO_DEEP

def check_hierarchy_depth(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    limit = getattr(runtime_ctx.validation, "max_hierarchy_depth", 10)

    if obj.max_depth > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_HIERARCHY_DEPTH_TOO_DEEP,
            severity=ValidationSeverity.WARNING,
            message=f"Hierarchy depth too deep: {obj.max_depth}",
            suggestion="Flatten overly nested structures."
        )
