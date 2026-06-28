from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_NON_MANIFOLD


def check_mesh_non_manifold(
    mesh: MeshContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue | None:

    if mesh.has_non_manifold_geo:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_NON_MANIFOLD,
            severity=ValidationSeverity.ERROR,
            message="Non-manifold geometry detected.",
            suggestion="Clean mesh topology to remove non-manifold elements."
        )

    return None