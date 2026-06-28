from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_NO_ROOT_OBJECTS

def check_no_root_objects(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    if len(obj.root_objects) == 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_NO_ROOT_OBJECTS,
            severity=ValidationSeverity.ERROR,
            message="Scene has no root objects.",
            suggestion="Ensure at least one root node exists."
        )