from core.validation_context import ValidationRuntimeContext
from core.validation_system import ValidationIssue, ValidationSeverity
from core.checks.validation_check_ids import CHECK_DUPLICATE_UV_SET_NAMES
from core.context.mesh_context import MeshContext


def check_duplicate_uv_set_names(mesh: MeshContext,
                                 runtime_ctx: ValidationRuntimeContext
                                 )-> ValidationIssue:

    uv_sets = mesh.uv_sets or []
    if len(set(uv_sets)) == len(uv_sets):
        return None

    return ValidationIssue(
        asset_name=mesh.name,
        check_name=CHECK_DUPLICATE_UV_SET_NAMES,
        severity=ValidationSeverity.WARNING,
        message="Mesh contains duplicate UV set names.",
        suggestion="Ensure UV set names are unique."
    )