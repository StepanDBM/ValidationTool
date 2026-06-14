from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_NGONS


def check_ngons(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if mesh.has_ngons:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_NGONS,
            severity=ValidationSeverity.WARNING,
            message="Mesh contains ngons which can cause issues in some game engines.",
            suggestion="Convert ngons to quads or tris."
        )
    return None