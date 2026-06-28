from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_ORPHAN_NODES

def check_orphan_nodes(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    if len(obj.root_objects) == len(obj.all_transforms) and len(obj.all_transforms) > 1:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_ORPHAN_NODES,
            severity=ValidationSeverity.WARNING,
            message="All objects are root-level (likely orphaned).",
            suggestion="Parent objects appropriately."
        )