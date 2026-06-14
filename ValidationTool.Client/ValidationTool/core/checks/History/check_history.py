from pathlib import Path
from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_HISTORY


def check_normals_exist(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    xtension = Path(mesh.path).suffix
    if xtension == ".ma" | xtension == ".mb":
        if mesh.has_history:
            return ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_HISTORY,
                severity=ValidationSeverity.WARNING,
                message="Mesh has construction history which can cause performance issues.",
                suggestion="Delete construction history for the mesh."
            )
    return None