from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_DEGENERATE_FACES

def check_mesh_degenerate_faces(
    mesh: MeshContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue | None:

    if mesh.has_degenerate_faces:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_DEGENERATE_FACES,
            severity=ValidationSeverity.ERROR,
            message="Degenerate faces detected.",
            suggestion="Remove or rebuild invalid or collapsed faces."
        )

    return None