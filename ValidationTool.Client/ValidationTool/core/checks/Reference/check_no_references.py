from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneReferenceContext import SceneReferenceContext

from core.checks.validation_check_ids import CHECK_NO_REFERENCES

def check_no_references(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneReferenceContext):
        return None

    if len(obj.references) == 0:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_NO_REFERENCES,
            severity=ValidationSeverity.INFO,
            message="Scene contains no references.",
            suggestion="Ensure references are used if required."
        )