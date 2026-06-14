from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_OVERLAPPING_GEOMETRY


def check_overlapping_geo(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_overlapping_geo:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_OVERLAPPING_GEOMETRY,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains overlapping geometry which can cause z-fighting.",
            suggestion="Identify and resolve overlapping faces in the mesh."
        )
    return None