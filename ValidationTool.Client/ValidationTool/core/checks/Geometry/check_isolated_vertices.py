from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_ISOLATED_VERTICES


def check_isolated_vertices(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_isolated_vertices:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_ISOLATED_VERTICES,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains isolated vertices that are not connected to any faces.",
                suggestion="Remove or connect isolated vertices to the mesh."
        )
    return None