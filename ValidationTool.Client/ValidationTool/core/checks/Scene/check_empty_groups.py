from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneHierarchyContext import SceneHierarchyContext

from core.checks.validation_check_ids import CHECK_EMPTY_GROUPS

def check_empty_groups(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneHierarchyContext):
        return None

    # groups without children are effectively empty
    if obj.groups and len(obj.groups) > 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_EMPTY_GROUPS,
            severity=ValidationSeverity.INFO,
            message=f"{len(obj.groups)} group nodes detected (may contain empties).",
            suggestion="Remove or consolidate empty group nodes."
        )