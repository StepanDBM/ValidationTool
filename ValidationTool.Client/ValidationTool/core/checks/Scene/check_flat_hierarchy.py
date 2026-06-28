from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_FLAT_HIERARCHY

def check_flat_hierarchy(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    if len(obj.root_objects) > 15 and obj.max_depth < 2:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_FLAT_HIERARCHY,
            severity=ValidationSeverity.INFO,
            message="Hierarchy is too flat.",
            suggestion="Introduce grouping for logical organization."
        )