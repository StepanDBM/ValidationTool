from typing import List

from core.context.mesh_context import MeshContext
from core.validation_system import AssetType, ObjectType

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _get_parent_path,
    _safe_list_connections,
    _safe_poly_uv_sets,
    _safe_scale,
    _safe_bbox,
    _safe_poly_evaluate
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def get_asset_type_from_name(name: str) -> AssetType:
    upper_name = name.upper()

    prefix_map = {
        ("CH_", "HERO_"): AssetType.CHARACTER,
        ("WP_", "WPN_"): AssetType.WEAPON,
        ("PRP_", "PROP_"): AssetType.PROP,
        ("MOD_",): AssetType.ENVIRONMENT_MODULAR,
        ("ENV_",): AssetType.ENVIRONMENT,
        ("VFX_", "FX_"): AssetType.VFX,
        ("VEH_", "VH_"): AssetType.VEHICLE,
        ("UI_",): AssetType.UI,
    }

    for prefixes, asset_type in prefix_map.items():
        if any(upper_name.startswith(prefix) for prefix in prefixes):
            return asset_type

    return AssetType.UNKNOWN

def extract_meshes() -> List[MeshContext]:
    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    mesh_shapes = cmds.ls(type="mesh", long=True) or []
    meshes: List[MeshContext] = []

    for shape in mesh_shapes:
        # Skip Maya intermediate shapes
        try:
            if cmds.getAttr(f"{shape}.intermediateObject"):
                continue
        except Exception:
            pass

        transform = cmds.listRelatives(shape, parent=True, fullPath=True)
        if not transform:
            continue

        transform = transform[0]
        asset_name = transform.split("|")[-1]
        asset_type = get_asset_type_from_name(asset_name)

        vertex_count = _safe_poly_evaluate(shape, "vertex")
        triangle_count = _safe_poly_evaluate(shape, "triangle")

        uv_sets = _safe_poly_uv_sets(shape)
        shading_groups = _safe_list_connections(shape, "shadingEngine")
        scale = _safe_scale(transform)
        bbox_min, bbox_max = _safe_bbox(shape)

        mesh = MeshContext(
            name=asset_name,
            object_type=ObjectType.MESH,
            path=transform,
            parent=_get_parent_path(transform),
            asset_type=asset_type,
            vertex_count=vertex_count,
            triangle_count=triangle_count,
            scale=scale,
            material_slot_count=len(shading_groups),
            has_ngons=False,
            ngons_quant=0,
            has_non_manifold_geo=False,
            has_zeroArea_faces=False,
            has_hidden_faces=False,
            hidden_faces_quant=0,
            has_isolated_vertices=False,
            isolated_faces_quant=0,
            has_lamina_faces=False,
            has_degenerate_faces=False,
            has_normals=True,
            has_broken_normals=False,
            has_overlapping_geo=False,
            bounding_box_min=bbox_min,
            bounding_box_max=bbox_max,
            collision_readiness=True,
            has_hard_edges=False,
            has_history=False,
            skeleton_name="",
            uv_sets=uv_sets,
            materials=shading_groups,
        )
        meshes.append(mesh)

    return meshes