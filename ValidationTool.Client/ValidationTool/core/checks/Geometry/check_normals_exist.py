from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_NORMALS


def check_normals_exist(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if not mesh.has_normals:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_NORMALS,
            severity=ValidationSeverity.WARNING,
            message="Mesh has party o completely lost its normals",
            suggestion="Recalculate or manually fix normals in the mesh."
        )
    return None