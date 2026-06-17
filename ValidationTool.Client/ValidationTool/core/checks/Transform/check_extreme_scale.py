from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.context.baseContext import BaseContext

from core.checks.validation_check_ids import (
    CHECK_EXTREME_SCALE,
)


MAX_SCALE = 1000.0

def check_extreme_scale(mObj: BaseContext,
                         context: ValidationRuntimeContext
                         ) -> ValidationIssue:
    if any(s > MAX_SCALE for s in mObj.scale):

        return(ValidationIssue(
            asset_name=mObj.name,
            check_name=CHECK_EXTREME_SCALE,
                severity=ValidationSeverity.WARNING,
                message=f"Extreme scale detected {mObj.scale}.",
                suggestion="Check asset scaling consistency."
        )
    )
