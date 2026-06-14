from core.validation_context import ValidationRuntimeContext
from core.validation_system import ValidationIssue, ValidationSeverity
from core.checks.validation_check_ids import CHECK_EMPTY_UV_SET_NAME
from core.context.mesh_context import MeshContext


def check_empty_uv_set_names(mesh: MeshContext,
                             runtime_ctx: ValidationRuntimeContext
                             ) -> ValidationIssue:

    uv_sets = mesh.uv_sets or []

    has_empty_name = any(not uv_set.strip() for uv_set in uv_sets)

    if not has_empty_name:
        return None

    return ValidationIssue(
        asset_name=mesh.name,
        check_name=CHECK_EMPTY_UV_SET_NAME,
        severity=ValidationSeverity.WARNING,
        message="Mesh contains unnamed UV sets.",
        suggestion="Rename UV sets properly."
    )