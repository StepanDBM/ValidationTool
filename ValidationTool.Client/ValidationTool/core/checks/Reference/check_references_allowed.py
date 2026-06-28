from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneReferenceContext import SceneReferenceContext

from core.checks.validation_check_ids import CHECK_REFERENCES_ALLOWED

def check_references_allowed(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneReferenceContext):
        return None

    allowed = getattr(runtime_ctx.validation, "references_allowed", True)

    if not allowed and obj.references:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_REFERENCES_ALLOWED,
            severity=ValidationSeverity.ERROR,
            message="References are not allowed in this pipeline.",
            suggestion="Remove references."
        )
