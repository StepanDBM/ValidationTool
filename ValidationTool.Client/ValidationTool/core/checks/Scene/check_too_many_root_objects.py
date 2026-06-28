from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_ROOT_OBJECTS

def check_too_many_root_objects(obj: BaseContext, runtime_ctx: ValidationRuntimeContext):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    limit = getattr(runtime_ctx.validation, "max_root_objects", 10)

    if len(obj.root_objects) > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_ROOT_OBJECTS,
            severity=ValidationSeverity.WARNING,
            message=f"Too many root objects: {len(obj.root_objects)}",
            suggestion="Group objects into a clearer hierarchy."
        )