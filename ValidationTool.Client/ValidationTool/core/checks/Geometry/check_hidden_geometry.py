from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_HIDDEN_GEOMETRY

def check_mesh_hidden_faces(
    mesh: MeshContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue | None:

    if mesh.has_hidden_faces:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_HIDDEN_GEOMETRY,
            severity=ValidationSeverity.WARNING,
            message=f"{mesh.hidden_faces_quant} hidden faces detected.",
            suggestion="Delete or reveal hidden faces before export."
        )

    return None