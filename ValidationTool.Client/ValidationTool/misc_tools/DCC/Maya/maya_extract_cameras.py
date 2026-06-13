from typing import List

from core.context.camera_context import CameraContext
from core.validation_system import ObjectType, AssetType

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _get_parent_path,
    _safe_get_vec3,
    _safe_get_float,
    _safe_get_bool
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def extract_cameras() -> List[CameraContext]:
    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    camera_shapes = cmds.ls(type="camera", long=True) or []
    cameras: List[CameraContext] = []

    for shape in camera_shapes:
        transform = cmds.listRelatives(shape, parent=True, fullPath=True)
        if not transform:
            continue

        transform = transform[0]
        camera_name = transform.split("|")[-1]

        position = _safe_get_vec3(f"{transform}.translate")
        rotation = _safe_get_vec3(f"{transform}.rotate")
        scale = _safe_get_vec3(f"{transform}.scale")

        focal_length = _safe_get_float(f"{shape}.focalLength", 35.0)
        near_clip = _safe_get_float(f"{shape}.nearClipPlane", 0.1)
        far_clip = _safe_get_float(f"{shape}.farClipPlane", 10000.0)

        is_renderable = _safe_get_bool(f"{shape}.renderable", False)
        is_orthographic = _safe_get_bool(f"{shape}.orthographic", False)
        camera_type = "ORTHOGRAPHIC" if is_orthographic else "PERSPECTIVE"

        camera = CameraContext(
            name=camera_name,
            object_type=ObjectType.CAMERA,
            path=transform,
            parent=_get_parent_path(transform),
            asset_type=AssetType.UNKNOWN,
            camera_type=camera_type,
            focal_length=focal_length,
            near_clip=near_clip,
            far_clip=far_clip,
            position=position,
            rotation=rotation,
            scale=scale,
            is_render_camera=is_renderable,
        )

        cameras.append(camera)

    return cameras
