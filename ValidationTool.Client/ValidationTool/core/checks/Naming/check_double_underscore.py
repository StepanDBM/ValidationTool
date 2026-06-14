from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
)
from core.checks.validation_check_ids import CHECK_DOUBLE_UNDERSCORE


def check_double_underscore(
    obj: BaseContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue:
    name = obj.name

    if "__" not in name:
        return None

    return ValidationIssue(
        asset_name=name,
        check_name=CHECK_DOUBLE_UNDERSCORE,
        severity=ValidationSeverity.WARNING,
        message="Object name contains double underscores.",
        suggestion="Avoid redundant separators in object names."
    )