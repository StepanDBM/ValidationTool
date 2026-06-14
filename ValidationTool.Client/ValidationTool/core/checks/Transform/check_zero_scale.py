from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.context.baseContext import BaseContext

from core.checks.validation_check_ids import (
    CHECK_NEGATIVE_SCALE,
)


def check_negative_scale(mObj: BaseContext,
                         context: ValidationRuntimeContext
                         ) -> ValidationIssue:
    if any(s == 0 for s in mObj.scale):

        return(ValidationIssue(
            asset_name=mObj.name,
            check_name=CHECK_NEGATIVE_SCALE,
            severity=ValidationSeverity.ERROR,
            message=f"Negative scale detected {mObj.scale}.",
            suggestion="Freeze transforms (scale). Beware of deformers and subsequent object inversions"
        )
    )
