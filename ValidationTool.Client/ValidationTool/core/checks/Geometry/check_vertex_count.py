from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_VERTEX_COUNT


def check_vertex_count(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:

    issue = None
    warning_limit = None
    error_limit = None

    limits = runtime_ctx.budgets.geometry
    if limits:
        warning_limit = limits.vertices_max
        error_limit = limits.vertices_max * 1.3
    else:
        return issue
    
    if mesh.vertex_count >= error_limit:
        print("First option")
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.ERROR,
                message=(
                    f"The vertex count {mesh.vertex_count} exceeds hard limit "
                    f"of {error_limit} for asset type {mesh.asset_type.value}"
                ),
                suggestion="Reduce mesh complexity."
            )
    elif mesh.vertex_count >= warning_limit:
        print("Seond option")
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"The vertex count ({mesh.vertex_count}) approaching limit "
                    f"between {warning_limit} - {error_limit}"
                ),
                suggestion="Review topology density."
            )
    elif mesh.vertex_count < 2:
        print("Third option")
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.HARD,
                message="Less than 2 vertices found in mesh, likely an import issue or corrupted file. Aborting further checks.",
                suggestion="Ensure the mesh has valid geometry."
            )
    return issue