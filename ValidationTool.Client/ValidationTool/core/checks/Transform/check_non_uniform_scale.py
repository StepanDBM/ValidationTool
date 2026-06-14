from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.context.baseContext import BaseContext

from core.checks.validation_check_ids import (
    CHECK_NON_UNIFORM_SCALE,
)

def check_negative_scale(mObj: BaseContext,
                         context: ValidationRuntimeContext
                         ) -> ValidationIssue:
    sx, sy, sz = mObj.scale

    if not (abs(sx - sy) < 1e-5 and abs(sy - sz) < 1e-5):

        return ValidationIssue(
            asset_name=mObj.name,
            check_name=CHECK_NON_UNIFORM_SCALE,
            severity=ValidationSeverity.WARNING,
            message=f"Non-uniform scale detected {mObj.scale}.",
            suggestion="Apply freeze transforms."
        )
