from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_ZERO_AREA_FACES


def check_zero_area_faces(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_zeroArea_faces:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_ZERO_AREA_FACES,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains zero-area faces which can cause rendering issues.",
            suggestion="Identify and fix zero-area faces in the mesh."
        )
    return None