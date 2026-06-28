from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_BROKEN_NORMALS


def check_broken_normals(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_broken_normals:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_BROKEN_NORMALS,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains normal issues such as flipped or inconsistent normals.",
            suggestion="Recalculate or manually fix normals in the mesh."
        )
    return None