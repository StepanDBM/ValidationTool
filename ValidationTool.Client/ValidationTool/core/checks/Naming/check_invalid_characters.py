from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
)
from core.checks.validation_check_ids import CHECK_INVALID_CHARACTERS


def check_invalid_characters(
    obj: BaseContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue:
    name = obj.name

    invalid_chars = []
    if " " in name:
        invalid_chars.append("space")
    if "." in name:
        invalid_chars.append("dot")

    if not invalid_chars:
        return None

    invalid_chars_text = ", ".join(invalid_chars)

    return ValidationIssue(
        asset_name=name,
        check_name=CHECK_INVALID_CHARACTERS,
        severity=ValidationSeverity.ERROR,
        message=f"Object name contains invalid characters: {invalid_chars_text}.",
        suggestion="Use underscores instead of spaces or dots."
    )