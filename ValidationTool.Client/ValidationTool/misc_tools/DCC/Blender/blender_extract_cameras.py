import bpy
from typing import List

from core.context.camera_context import CameraContext
from core.validation_system import ObjectType, AssetType


def _get_parent_path(obj: bpy.types.Object) -> str:
    if obj.parent is None:
        return ""
    return obj.parent.name_full


def _get_camera_type(camera_data: bpy.types.Camera) -> str:
    if camera_data.type == "ORTHO":
        return "ORTHOGRAPHIC"
    if camera_data.type == "PANO":
        return "PANORAMIC"
    return "PERSPECTIVE"


def extract_cameras() -> List[CameraContext]:
    cameras: List[CameraContext] = []

    scene_camera = bpy.context.scene.camera

    for obj in bpy.context.scene.objects:
        if obj.type != "CAMERA":
            continue

        camera_data = obj.data

        camera = CameraContext(
            name=obj.name,
            object_type=ObjectType.CAMERA,
            path=obj.name_full,
            parent=_get_parent_path(obj),
            asset_type=AssetType.UNKNOWN,
            camera_type=_get_camera_type(camera_data),
            focal_length=float(camera_data.lens),
            near_clip=float(camera_data.clip_start),
            far_clip=float(camera_data.clip_end),
            position=tuple(obj.location),
            rotation=tuple(obj.rotation_euler),
            scale=tuple(obj.scale),
            is_render_camera=(scene_camera == obj) and (not obj.hide_render),
        )

        cameras.append(camera)

    return cameras