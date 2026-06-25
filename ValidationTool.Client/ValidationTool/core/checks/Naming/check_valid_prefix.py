from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
)
from core.checks.validation_check_ids import CHECK_VALID_PREFIX


def check_valid_prefix(
        obj: BaseContext,
        runtime_ctx: ValidationRuntimeContext
        ) -> ValidationIssue:

    name = obj.name
    upper_name = name.upper()
    valid_prefixes = runtime_ctx.naming.valid_prefixes or []

    has_valid_prefix = any(
        upper_name.startswith(prefix.upper() + "_")
        for prefix in valid_prefixes
    )

    if has_valid_prefix:
        return None

    return ValidationIssue(
        asset_name=name,
        check_name=CHECK_VALID_PREFIX,
        severity=ValidationSeverity.WARNING,
        message="Object missing valid asset prefix.",
        suggestion="Use prefixes like CH_, ENV_, PRP_, WPN_, etc."
    )