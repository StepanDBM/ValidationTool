from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_LAMINA_FACES


def check_mesh_lamina_faces(
    mesh: MeshContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue | None:

    if mesh.has_lamina_faces:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_LAMINA_FACES,
            severity=ValidationSeverity.ERROR,
            message="Lamina faces detected.",
            suggestion="Remove overlapping faces sharing the same space."
        )

    return None