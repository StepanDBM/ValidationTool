
from typing import List

from  mathutils import Vector

import bpy

import sys
import os
print("SCRIPT RUNNING")
script_dir = r"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool"

if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.validation_system import MeshContext, AssetType


def get_asset_type_from_name(name: str) -> "AssetType":
    name = name.upper()

    if name.startswith("CH_") or name.startswith("HERO_"):
        return AssetType.CHARACTER

    elif name.startswith("WP_") or name.startswith("WPN_"):
        return AssetType.WEAPON

    elif name.startswith("PROP_") or name.startswith("PRP_"):
        return AssetType.PROP

    elif name.startswith("MOD_") or name.startswith("ENV_"):
        return AssetType.ENVIRONMENT_MODULAR

    return AssetType.UNKNOWN


def extract_meshes_from_scene() -> List["MeshContext"]:
    meshes: List[MeshContext] = []

    for obj in bpy.context.scene.objects:

        if obj.type != 'MESH':
            continue

        mesh = obj.data

        asset_name = obj.name
        asset_type = get_asset_type_from_name(asset_name)

        # -------------------------
        # Geometry stats
        # -------------------------
        vertex_count = len(mesh.vertices)
        print("vertex count:", vertex_count)
        triangle_count = len(mesh.polygons)
        print("triangle count:", triangle_count)

        # -------------------------
        # UVs
        # -------------------------
        uv_layers = mesh.uv_layers
        uv_sets = [uv.name for uv in uv_layers] if uv_layers else []

        has_uv0 = len(uv_sets) > 0
        has_uv1 = len(uv_sets) > 1

        print("UV sets:", uv_sets)
        print("Has UV0:", has_uv0)
        print("Has UV1:", has_uv1)

        # -------------------------
        # Materials
        # -------------------------
        material_slots = obj.material_slots
        materials = [
            slot.material.name
            for slot in material_slots
            if slot.material
        ]
        material_count = len(materials)
        print("Material count:", material_count)

        # -------------------------
        # Transform / scale
        # -------------------------
        scale = tuple(obj.scale)
        has_negative_scale = any(s < 0 for s in scale)
        print("Scale:", scale)
        print("Has negative scale:", has_negative_scale)

        # -------------------------
        # Bounding box (world space)
        # -------------------------
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

        min_x = min(v.x for v in bbox_corners)
        min_y = min(v.y for v in bbox_corners)
        min_z = min(v.z for v in bbox_corners)

        max_x = max(v.x for v in bbox_corners)
        max_y = max(v.y for v in bbox_corners)
        max_z = max(v.z for v in bbox_corners)

        bounding_box_min = (min_x, min_y, min_z)
        bounding_box_max = (max_x, max_y, max_z)

        # -------------------------
        # MeshContext output
        # -------------------------
        mesh_context = MeshContext(
            name=asset_name,
            asset_type=asset_type,

            vertex_count=vertex_count,
            triangle_count=triangle_count,

            scale=scale,

            material_slot_count=material_count,

            has_uv0=has_uv0,
            has_uv1=has_uv1,

            has_negative_scale=has_negative_scale,

            has_non_manifold_geo=False,  # placeholder
            has_degenerate_faces=False,   # placeholder

            bounding_box_min=bounding_box_min,
            bounding_box_max=bounding_box_max,

            uv_sets=uv_sets,
            materials=materials
        )

        meshes.append(mesh_context)

    return meshes