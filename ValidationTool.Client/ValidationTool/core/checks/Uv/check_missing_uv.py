from core.validation_context import ValidationRuntimeContext
from core.validation_system import ValidationIssue, ValidationSeverity
from core.checks.validation_check_ids import (
    CHECK_MISSING_UV0,
    CHECK_MISSING_UV1,
    CHECK_TOO_MANY_UV_SETS
)
from core.context.mesh_context import MeshContext

EXPCT_UV_SETS = 2 #should be the runtime_ctx who decides this, but UI is too coupled now... Let's wait for now.
# 2 is a nice value to begin with.
def check_missing_uvs(
        mesh: MeshContext,
        runtime_ctx: ValidationRuntimeContext
        ) -> ValidationIssue:
    if len(mesh.uv_sets) == 0:
        return ValidationIssue( 
            asset_name=mesh.name,
            check_name=CHECK_MISSING_UV0,
            severity=ValidationSeverity.ERROR,
            message="Missing ALL UV sets.",
            suggestion="Create at least one valid UV layout."
        )
    elif len(mesh.uv_sets) < EXPCT_UV_SETS:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_MISSING_UV1,
            severity=ValidationSeverity.WARNING,
            message="Missing secondary UV set (UV1).",
            suggestion="Create a valid UV layout."
        )
    elif len(mesh.uv_sets) > EXPCT_UV_SETS:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_TOO_MANY_UV_SETS,
            severity=ValidationSeverity.ERROR,
            message="Missing primary UV set (UV0).",
            suggestion="Create a valid UV layout."
        )