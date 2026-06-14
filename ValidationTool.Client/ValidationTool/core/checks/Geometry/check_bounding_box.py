from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity,
    AssetType,
)

from core.checks.validation_check_ids import CHECK_BOUNDING_BOX


DEFAULT_MAX_BBOX_SIZE = 100.0
DEFAULT_MIN_BBOX_SIZE = 0.0001


def _get_limits_for_asset_type(asset_type: AssetType, budgets):
    if budgets is None:
        return None

    if asset_type == AssetType.CHARACTER:
        return getattr(budgets, "character", None)
    elif asset_type == AssetType.WEAPON:
        return getattr(budgets, "weapon", None)
    elif asset_type == AssetType.PROP:
        return getattr(budgets, "prop", None)
    elif asset_type == AssetType.ENVIRONMENT_MODULAR:
        return getattr(budgets, "environment", None)
    elif asset_type == AssetType.VEHICLE:
        return getattr(budgets, "vehicle", None)

    return None


def check_bounding_box(
    mesh: MeshContext,
    runtime_ctx: ValidationRuntimeContext
) -> ValidationIssue | None:
    bbox_min = mesh.bounding_box_min
    bbox_max = mesh.bounding_box_max

    if not bbox_min or not bbox_max or len(bbox_min) != 3 or len(bbox_max) != 3:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_BOUNDING_BOX,
            severity=ValidationSeverity.ERROR,
            message="Mesh bounding box data is missing or invalid.",
            suggestion="Recompute or re-export valid bounding box data."
        )

    size_x = bbox_max[0] - bbox_min[0]
    size_y = bbox_max[1] - bbox_min[1]
    size_z = bbox_max[2] - bbox_min[2]

    if size_x < 0 or size_y < 0 or size_z < 0:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_BOUNDING_BOX,
            severity=ValidationSeverity.ERROR,
            message=(
                f"Invalid bounding box extents detected: "
                f"min={bbox_min}, max={bbox_max}."
            ),
            suggestion="Validate transform freeze/export order and bounding box extraction."
        )

    limits = _get_limits_for_asset_type(mesh.asset_type, runtime_ctx.budgets)

    max_bbox_size = DEFAULT_MAX_BBOX_SIZE
    min_bbox_size = DEFAULT_MIN_BBOX_SIZE

    if limits is not None:
        max_bbox_size = getattr(limits, "max_bbox_size", DEFAULT_MAX_BBOX_SIZE)
        min_bbox_size = getattr(limits, "min_bbox_size", DEFAULT_MIN_BBOX_SIZE)

    if size_x <= min_bbox_size and size_y <= min_bbox_size and size_z <= min_bbox_size:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_BOUNDING_BOX,
            severity=ValidationSeverity.ERROR,
            message=(
                f"Mesh bounding box is near zero size: "
                f"({size_x:.6f}, {size_y:.6f}, {size_z:.6f})."
            ),
            suggestion="Check for collapsed geometry, invalid scale, or export issues."
        )

    if size_x > max_bbox_size or size_y > max_bbox_size or size_z > max_bbox_size:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_BOUNDING_BOX,
            severity=ValidationSeverity.WARNING,
            message=(
                f"Mesh bounding box exceeds expected size: "
                f"({size_x:.3f}, {size_y:.3f}, {size_z:.3f}) "
                f"max allowed {max_bbox_size}."
            ),
            suggestion="Verify asset scale, scene units, and pivot placement."
        )

    return None