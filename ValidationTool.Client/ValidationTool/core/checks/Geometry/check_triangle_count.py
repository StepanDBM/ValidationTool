from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_TRIANGLE_COUNT



def check_triangle_count(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    issue = None
    warning_limit = None
    error_limit = None
    limits = runtime_ctx.budgets.geometry
    if limits:
        warning_limit = limits.triangles_max
        error_limit = limits.triangles_max * 1.3
    else:
        return issue

    if mesh.triangle_count >= error_limit:
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_TRIANGLE_COUNT,
                severity=ValidationSeverity.ERROR,
                message=(
                    f"Triangle count {mesh.triangle_count} exceeds hard limit "
                    f"of {error_limit} for asset type {mesh.asset_type.value}"
                ),
                suggestion="Reduce mesh complexity."
            )
    elif mesh.triangle_count >= warning_limit:
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_TRIANGLE_COUNT,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Triangle count ({mesh.triangle_count}) approaching limit "
                    f"between {warning_limit} - {error_limit}"
                ),
                suggestion="Review topology density."
            )
    return issue
