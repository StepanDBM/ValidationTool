from typing import List

from core.context.light_context import LightContext
from core.validation_system import ObjectType, AssetType

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _get_parent_path,
    _safe_get_vec3,
    _safe_get_float,
    _safe_get_bool,
    _safe_get_color,
    _get_light_type,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


ARNOLD_LIGHT_NODE_TYPES = [
    "aiAreaLight",
    "aiSkyDomeLight",
    "aiPhotometricLight",
    "aiMeshLight",
]

def _collect_light_shapes() -> list[str]:
    native_lights = cmds.ls(lights=True, long=True) or []

    arnold_lights = []
    for node_type in ARNOLD_LIGHT_NODE_TYPES:
        arnold_lights.extend(cmds.ls(type=node_type, long=True) or [])

    all_lights = native_lights + arnold_lights

    # deduplicate while preserving order
    seen = set()
    unique = []
    for item in all_lights:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique


def extract_lights() -> List[LightContext]:
    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    light_shapes = _collect_light_shapes()
    lights: List[LightContext] = []

    for shape in light_shapes:
        transform = cmds.listRelatives(shape, parent=True, fullPath=True)
        if not transform:
            continue

        transform = transform[0]
        light_name = transform.split("|")[-1]

        position = _safe_get_vec3(f"{transform}.translate")
        rotation = _safe_get_vec3(f"{transform}.rotate")
        scale = _safe_get_vec3(f"{transform}.scale")

        intensity = _safe_get_float(f"{shape}.intensity", 1.0)
        color = _safe_get_color(f"{shape}.color")

        emits_diffuse = _safe_get_bool(f"{shape}.emitDiffuse", True)
        emits_specular = _safe_get_bool(f"{shape}.emitSpecular", True)

        casts_shadows = False
        shadow_attrs = [
            f"{shape}.useDepthMapShadows",
            f"{shape}.useRayTraceShadows",
            f"{shape}.aiCastShadows",
            f"{shape}.castShadows",
        ]

        for attr in shadow_attrs:
            if cmds.objExists(attr):
                casts_shadows = _safe_get_bool(attr, False)
                if casts_shadows:
                    break

        enabled = True
        if cmds.objExists(f"{shape}.visibility"):
            enabled = _safe_get_bool(f"{shape}.visibility", True)

        light = LightContext(
            name=light_name,
            object_type=ObjectType.LIGHT,
            path=transform,
            parent=_get_parent_path(transform),
            asset_type=AssetType.UNKNOWN,
            light_type=_get_light_type(shape),
            intensity=intensity,
            color=color,
            position=position,
            rotation=rotation,
            scale=scale,
            casts_shadows=casts_shadows,
            emits_diffuse=emits_diffuse,
            emits_specular=emits_specular,
            enabled=enabled,
        )

        lights.append(light)

    return lights