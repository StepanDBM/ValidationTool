from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_HARD_EDGES


def check_hard_edges(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_hard_edges:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_HARD_EDGES,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains hard edges which may affect shading.",
            suggestion="Review and adjust hard edge settings as needed."
        )
    return None