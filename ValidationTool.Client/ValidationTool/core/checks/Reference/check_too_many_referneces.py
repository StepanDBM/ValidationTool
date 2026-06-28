from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneReferenceContext import SceneReferenceContext

from core.checks.validation_check_ids import CHECK_TOO_MANY_REFERENCES

def check_too_many_references(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneReferenceContext):
        return None

    limit = getattr(runtime_ctx.validation, "max_references", 20)

    if len(obj.references) > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_TOO_MANY_REFERENCES,
            severity=ValidationSeverity.WARNING,
            message=f"Too many references: {len(obj.references)}",
            suggestion="Reduce dependencies."
        )
