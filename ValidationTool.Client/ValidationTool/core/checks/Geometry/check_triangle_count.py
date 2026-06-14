from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
    AssetType
)

from core.checks.validation_check_ids import CHECK_TRIANGLE_COUNT

def getLimitsForAssetType(asset_type: AssetType, budgets):
    if asset_type == AssetType.STATIC_MESH:
        return budgets.static_mesh
    elif asset_type == AssetType.CHARACTER:
        return budgets.character
    elif asset_type == AssetType.WEAPON:
        return budgets.weapon
    elif asset_type == AssetType.PROP:
        return budgets.prop
    elif asset_type == AssetType.ENVIRONMENT_MODULAR:
        return budgets.environment
    else:
        return None
def check_triangle_count(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    issue = None
    warning_limit = None
    error_limit = None
    limits = getLimitsForAssetType(mesh.asset_type, runtime_ctx.budgets)
    if limits:
        warning_limit = limits.max_triangles
        error_limit = limits.max_triangles * 1.3
    else:
        return issue

    if mesh.triangle_count >= error_limit:
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_TRIANGLE_COUNT,
                severity=ValidationSeverity.ERROR,
                message=(
                    f"Triangle count {mesh.triangle_count} exceeds hard limit "
                    f"of {error_limit} for asset type {mesh.asset_type.value}"
                ),
                suggestion="Reduce mesh complexity."
            )
    elif mesh.triangle_count >= warning_limit:
        issue = ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_TRIANGLE_COUNT,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Triangle count ({mesh.triangle_count}) approaching limit "
                    f"between {warning_limit} - {error_limit}"
                ),
                suggestion="Review topology density."
            )
    return issue
