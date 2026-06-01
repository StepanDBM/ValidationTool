from typing import List

from core.validation_system import (
    MeshContext,
    ValidationIssue,
    ValidationSeverity,
    AssetType,
    CHECK_VERTEX_COUNT,
    CHECK_TRIANGLE_COUNT,
    CHECK_NON_MANIFOLD,
    CHECK_DEGENERATE_FACES,
    CHECK_TRANSFORMS,
    CHECK_BOUNDING_BOX,
    CHECK_MATERIAL_SLOTS,
    CHECK_UV_SETS,
    CHECK_NAMING
)

from config.mesh_budgets import (
    CHARACTER_BUDGET,
    STATIC_MESH_BUDGET,
    WEAPON_BUDGET,
    PROP_BUDGET,
    ENVIRONMENT_BUDGET
)

def getLimitsForAssetType(asset_type: AssetType):
    if asset_type == AssetType.STATIC_MESH:
        return STATIC_MESH_BUDGET
    elif asset_type == AssetType.CHARACTER:
        return CHARACTER_BUDGET
    elif asset_type == AssetType.WEAPON:
        return WEAPON_BUDGET
    elif asset_type == AssetType.PROP:
        return PROP_BUDGET
    elif asset_type == AssetType.ENVIRONMENT_MODULAR:
        return ENVIRONMENT_BUDGET
    else:
        return None

def check_vertex_count(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []
    warning_limit = None
    error_limit = None
    limits = getLimitsForAssetType(mesh.asset_type)
    #print("ENUM OBJECT:", mesh.asset_type, id(mesh.asset_type))
    #print("REFERENCE:", AssetType.CHARACTER, id(AssetType.CHARACTER))
    #print("EQUAL:", mesh.asset_type == AssetType.CHARACTER)
    if limits:
        warning_limit = limits.max_vertices
        error_limit = limits.max_vertices * 1.3
    else:
        return issues
    
    if mesh.vertex_count >= error_limit:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.ERROR,
                message=(
                    f"The vertex count {mesh.vertex_count} exceeds hard limit "
                    f"of {error_limit} for asset type {mesh.asset_type.value}"
                ),
                suggestion="Reduce mesh complexity."
            )
        )
    elif mesh.vertex_count >= warning_limit:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Vertex count ({mesh.vertex_count}) approaching limit "
                    f"between {warning_limit} - {error_limit}"
                ),
                suggestion="Review topology density."
            )
        )
    elif mesh.vertex_count < 2:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.ERROR_HARD,
                message="Less than 2 vertices found in mesh, likely an import issue or corrupted file. Aborting further checks.",
                suggestion="Ensure the mesh has valid geometry."
            )
        )
    else:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_VERTEX_COUNT,
                severity=ValidationSeverity.INFO,
                message=(
                    f"Vertex count within acceptable range "
                    f"({mesh.vertex_count})"
                )
            )
        )
    return issues

def check_triangle_count(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []


    warning_limit = None
    error_limit = None
    limits = getLimitsForAssetType(mesh.asset_type)
    if limits:
        warning_limit = limits.max_triangles
        error_limit = limits.max_triangles * 1.3
    else:
        return issues

    if mesh.triangle_count >= error_limit:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_TRIANGLE_COUNT",
                severity=ValidationSeverity.ERROR,
                message=(
                    f"Triangle count {mesh.triangle_count} exceeds hard limit "
                    f"of {error_limit} for asset type {mesh.asset_type.value}"
                ),
                suggestion="Reduce mesh complexity."
            )
        )
    elif mesh.triangle_count >= warning_limit:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_TRIANGLE_COUNT",
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Triangle count ({mesh.triangle_count}) approaching limit "
                    f"between {warning_limit} - {error_limit}"
                ),
                suggestion="Review topology density."
            )
        )
    else:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_TRIANGLE_COUNT",
                severity=ValidationSeverity.INFO,
                message=(
                    f"Triangle count within acceptable range "
                    f"({mesh.triangle_count})"
                )
            )
        )
    return issues


def check_zero_area_faces(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for zero-area face detection
    has_zero_area_faces = False  # This would be determined by actual geometry analysis

    if has_zero_area_faces:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_ZERO_AREA_FACES",
                severity=ValidationSeverity.WARNING,
                message="Mesh contains zero-area faces which can cause rendering issues.",
                suggestion="Identify and fix zero-area faces in the mesh."
            )
        )

    return issues

def check_ngons(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for ngon detection
    has_ngons = False  # This would be determined by actual geometry analysis

    if has_ngons:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_NGONS",
                severity=ValidationSeverity.WARNING,
                message="Mesh contains ngons which can cause issues in some game engines.",
                suggestion="Convert ngons to quads or tris."
            )
        )

    return issues

def check_isolated_vertices(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for isolated vertex detection
    has_isolated_vertices = False  # This would be determined by actual geometry analysis

    if has_isolated_vertices:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_ISOLATED_VERTICES",
                severity=ValidationSeverity.INFO,
                message="Mesh contains isolated vertices that are not connected to any faces.",
                suggestion="Remove or connect isolated vertices to the mesh."
            )
        )

    return issues

def check_overlapping_geometry(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for overlapping geometry detection
    has_overlapping_geometry = False  # This would be determined by actual geometry analysis

    if has_overlapping_geometry:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_OVERLAPPING_GEOMETRY",
                severity=ValidationSeverity.WARNING,
                message="Mesh contains overlapping geometry which can cause z-fighting.",
                suggestion="Identify and resolve overlapping faces in the mesh."
            )
        )

    return issues

def check_normals(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for normal issues detection
    has_normal_issues = False  # This would be determined by actual geometry analysis

    if has_normal_issues:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_NORMALS",
                severity=ValidationSeverity.INFO,
                message="Mesh contains normal issues such as flipped or inconsistent normals.",
                suggestion="Recalculate or manually fix normals in the mesh."
            )
        )

    return issues

def check_hard_edges(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for hard edge detection
    has_hard_edges = False  # This would be determined by actual geometry analysis

    if has_hard_edges:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_HARD_EDGES",
                severity=ValidationSeverity.INFO,
                message="Mesh contains hard edges which may affect shading.",
                suggestion="Review and adjust hard edge settings as needed."
            )
        )

    return issues

def check_history(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for construction history detection
    has_history = False  # This would be determined by actual scene analysis

    if has_history:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_HISTORY",
                severity=ValidationSeverity.INFO,
                message="Mesh has construction history which can cause performance issues.",
                suggestion="Delete construction history for the mesh."
            )
        )

    return issues

def check_lamina_faces(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for lamina face detection
    has_lamina_faces = False  # This would be determined by actual geometry analysis

    if has_lamina_faces:
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_LAMINA_FACES",
                severity=ValidationSeverity.INFO,
                message="Mesh contains lamina faces which are faces that share all vertices with another face.",
                suggestion="Identify and resolve lamina faces in the mesh."
            )
        )

    return issues

def material_slots(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for material slot count check
    if mesh.material_slot_count > 4:  # Example threshold
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_MATERIAL_SLOTS",
                severity=ValidationSeverity.WARNING,
                message=f"Mesh has {mesh.material_slot_count} material slots which may exceed engine limits.",
                suggestion="Reduce the number of material slots used by the mesh."
            )
        )

    return issues

def check_boundingBox(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []

    # Placeholder logic for bounding box size check
    max_size = 100.0  # Example maximum size threshold
    bbox_size = (
        mesh.bounding_box_max[0] - mesh.bounding_box_min[0],
        mesh.bounding_box_max[1] - mesh.bounding_box_min[1],
        mesh.bounding_box_max[2] - mesh.bounding_box_min[2]
    )
    if any(size > max_size for size in bbox_size):
        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name="CHECK_BOUNDING_BOX",
                severity=ValidationSeverity.WARNING,
                message=f"Mesh has a bounding box size of {bbox_size} which may be too large for the target engine.",
                suggestion="Scale down the mesh or adjust its pivot to reduce bounding box size."
            )
        )

    return issues