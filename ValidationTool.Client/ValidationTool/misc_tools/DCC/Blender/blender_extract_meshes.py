import bpy
from typing import List
from mathutils import Vector

from core.context.mesh_context import MeshContext
from core.validation_system import AssetType, ObjectType

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _get_parent_path,
    _safe_count_ngons,
    _safe_has_non_manifold,
    _safe_has_lamina_faces,
    _safe_count_zero_area_faces,
    _safe_has_history,
    _safe_count_hard_edges,
    _safe_has_normals,
    _safe_count_hidden_faces,
    _safe_count_isolated_vertices,
    _safe_count_degenerate_faces,
    _safe_has_broken_normals,
    _safe_has_overlapping_geo
)

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


def _get_parent_path(obj: bpy.types.Object) -> str:
    if obj.parent is None:
        return ""
    return obj.parent.name_full


def _get_bbox_world(obj: bpy.types.Object) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    min_x = min(v.x for v in bbox_corners)
    min_y = min(v.y for v in bbox_corners)
    min_z = min(v.z for v in bbox_corners)

    max_x = max(v.x for v in bbox_corners)
    max_y = max(v.y for v in bbox_corners)
    max_z = max(v.z for v in bbox_corners)

    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def _get_triangle_count(mesh: bpy.types.Mesh) -> int:
    return sum(len(poly.vertices) - 2 for poly in mesh.polygons if len(poly.vertices) >= 3)


def extract_meshes() -> List[MeshContext]:
    meshes: List[MeshContext] = []

    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue

        mesh = obj.data
        asset_name = obj.name
        asset_type = get_asset_type_from_name(asset_name)

        vertex_count = len(mesh.vertices)
        triangle_count = _get_triangle_count(mesh)

        uv_layers = mesh.uv_layers
        uv_sets = [uv.name for uv in uv_layers] if uv_layers else []

        material_slots = obj.material_slots
        materials = [
            slot.material.name
            for slot in material_slots
            if slot.material is not None
        ]

        scale = tuple(obj.scale)
        bbox_min, bbox_max = _get_bbox_world(obj)

        ngons_count = _safe_count_ngons(obj)
        zero_area_count = _safe_count_zero_area_faces(obj)
        hard_edges_count = _safe_count_hard_edges(obj)

        has_non_manifold = _safe_has_non_manifold(obj)
        has_lamina = _safe_has_lamina_faces(obj)
        has_history = _safe_has_history(obj)
        has_normals = _safe_has_normals(obj)

        hidden_faces_count = _safe_count_hidden_faces(obj)
        isolated_vertices_count = _safe_count_isolated_vertices(obj)
        degenerate_faces_count = _safe_count_degenerate_faces(obj)

        has_broken_normals = _safe_has_broken_normals(obj)
        has_overlapping_geo = _safe_has_overlapping_geo(obj)

        mesh_context = MeshContext(
            name=asset_name,
            object_type=ObjectType.MESH,
            path=obj.name_full,
            parent=_get_parent_path(obj),
            asset_type=asset_type,
            vertex_count=vertex_count,
            triangle_count=triangle_count,
            scale=scale,
            material_slot_count=len(materials),
            has_ngons=ngons_count>0,
            ngons_quant=ngons_count,
            has_non_manifold_geo=has_non_manifold,
            has_zeroArea_faces=zero_area_count>0,
            zeroArea_quant=zero_area_count,
            has_hidden_faces=hidden_faces_count>0,
            hidden_faces_quant=hidden_faces_count,
            has_isolated_vertices=isolated_vertices_count>0,
            isolated_faces_quant=isolated_vertices_count,
            has_lamina_faces=has_lamina,
            has_degenerate_faces=degenerate_faces_count>0,
            has_normals=has_normals,
            has_broken_normals=has_broken_normals,
            has_overlapping_geo=has_overlapping_geo,
            bounding_box_min=bbox_min,
            bounding_box_max=bbox_max,
            collision_readiness=True,
            has_hard_edges=hard_edges_count>0,
            hard_edges_count=hard_edges_count,
            has_history=has_history,
            skeleton_name="",
            uv_sets=uv_sets,
            materials=materials
        )

        meshes.append(mesh_context)

    return meshes
