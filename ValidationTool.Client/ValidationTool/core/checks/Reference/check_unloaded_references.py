from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneReferenceContext import SceneReferenceContext

from core.checks.validation_check_ids import CHECK_UNLOADED_REFERENCES

def check_unloaded_references(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneReferenceContext):
        return None

    if obj.unloaded_references:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_UNLOADED_REFERENCES,
            severity=ValidationSeverity.WARNING,
            message=f"{len(obj.unloaded_references)} unloaded references.",
            suggestion="Load or remove unused references."
        )
