from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
)
from core.checks.validation_check_ids import CHECK_NAME_PATTERN


def check_name_pattern(
        obj: BaseContext, 
        runtime_ctx: ValidationRuntimeContext
        ) -> ValidationIssue:
    name = obj.name
    pattern = runtime_ctx.naming_rules.name_pattern

    if pattern.match(name):
        return None

    return ValidationIssue(
        asset_name=name,
        check_name=CHECK_NAME_PATTERN,
        severity=ValidationSeverity.WARNING,
        message=f"Object name does not follow naming convention: {name}",
        suggestion="Use the configured naming pattern, e.g. PREFIX_AssetName."
    )