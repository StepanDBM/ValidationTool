from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_EMPTY_TRANSFORMS

def check_empty_transforms(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    if obj.empty_transforms:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_EMPTY_TRANSFORMS,
            severity=ValidationSeverity.WARNING,
            message=f"{len(obj.empty_transforms)} empty transforms found.",
            suggestion="Delete unused transforms."
        )
