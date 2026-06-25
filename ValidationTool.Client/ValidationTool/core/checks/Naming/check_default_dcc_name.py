from core.context.baseContext import BaseContext
from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
)
from core.checks.validation_check_ids import CHECK_DEFAULT_DCC_NAMING

def check_default_dcc_naming(
        obj: BaseContext,
        runtime_ctx: ValidationRuntimeContext
        ) -> ValidationIssue:

    name = obj.name
    default_names = runtime_ctx.naming.default_maya_names or []

    for default_name in default_names:
        if name.startswith(default_name):
            return ValidationIssue(
                asset_name=name,
                check_name=CHECK_DEFAULT_DCC_NAMING,
                severity=ValidationSeverity.WARNING,
                message=f"Object uses default DCC naming: {name}",
                suggestion="Rename object using studio naming conventions."
            )
    return None