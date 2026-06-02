from typing import List
from core.validation_system import MeshContext, AssetType

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None
def getAssetTypeFromName(name: str) -> AssetType:

    name = name.upper()

    if name.startswith("CH_") or name.startswith("HERO_"):
        return AssetType.CHARACTER

    elif name.startswith("WP_") or name.startswith("WPN_"):
        return AssetType.WEAPON

    elif name.startswith("PROP_") or name.startswith("PRP_"):
        return AssetType.PROP

    elif name.startswith("MOD_") or name.startswith("ENV_"):
        return AssetType.ENVIRONMENT_MODULAR

    else:
        return AssetType.UNKNOWN
    
def extract_meshes_from_scene() -> List[MeshContext]:

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")
    mesh_shapes = cmds.ls(type="mesh", long=True) or []
    meshes: List[MeshContext] = []

    for shape in mesh_shapes:
        transform = cmds.listRelatives(shape,
                                       parent=True,
                                       fullPath=True)
        if not transform:
            continue
        transform = transform[0]
        asset_name = transform.split("|")[-1]
        myAssetType = getAssetTypeFromName(asset_name)
        
        vertex_count = cmds.polyEvaluate(shape, vertex=True)
        face_count = cmds.polyEvaluate(shape, face=True)

        uv_sets = cmds.polyUVSet(shape, query=True, allUVSets=True) or []
        has_uv0 = len(uv_sets) > 0
        has_uv1 = len(uv_sets) > 1

        shading_groups = cmds.listConnections(shape, type="shadingEngine") or []
        material_count = len(shading_groups)

        scale = cmds.getAttr(transform + ".scale")[0]
        has_negative_scale = any(s < 0 for s in scale)

        bbox = cmds.exactWorldBoundingBox(shape)

        bounding_box_min = (bbox[0], bbox[1], bbox[2])
        bounding_box_max = (bbox[3], bbox[4], bbox[5])
        mesh = MeshContext(
            name=asset_name,
            asset_type=myAssetType,

            vertex_count=vertex_count,
            triangle_count=face_count,

            scale=scale,

            material_slot_count=material_count,

            has_uv0=has_uv0,
            has_uv1=has_uv1,

            has_negative_scale=has_negative_scale,
            has_non_manifold_geo=False,   # placeholder (needs poly cleanup checks)
            has_degenerate_faces=False,   # placeholder

            bounding_box_min=bounding_box_min,
            bounding_box_max=bounding_box_max,

            uv_sets=uv_sets,
            materials=shading_groups
        )
        meshes.append(mesh)

    return meshes