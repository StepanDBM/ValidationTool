from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneReferenceContext import SceneReferenceContext

from core.checks.validation_check_ids import CHECK_BROKEN_REFERENCES

def check_broken_references(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneReferenceContext):
        return None

    if obj.broken_references:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_BROKEN_REFERENCES,
            severity=ValidationSeverity.ERROR,
            message=f"{len(obj.broken_references)} broken references.",
            suggestion="Fix or remove broken references."
        )