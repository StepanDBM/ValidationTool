from typing import List

from core.context.light_context import LightContext
from core.validation_system import ObjectType, AssetType

try:
    import bpy
except ImportError:
    bpy = None


def _get_parent_path(obj) -> str:
    parents = []
    current = getattr(obj, "parent", None)

    while current is not None:
        parents.append(current.name)
        current = getattr(current, "parent", None)

    parents.reverse()
    return "|".join(parents)


def _get_object_path(obj) -> str:
    parent_path = _get_parent_path(obj)
    if parent_path:
        return f"{parent_path}|{obj.name}"
    return obj.name


def _safe_vec3(value) -> tuple[float, float, float]:
    try:
        return (float(value[0]), float(value[1]), float(value[2]))
    except Exception:
        return (0.0, 0.0, 0.0)


def _safe_color(value) -> tuple[float, float, float]:
    try:
        return (float(value[0]), float(value[1]), float(value[2]))
    except Exception:
        return (1.0, 1.0, 1.0)


def _get_light_type(light_data) -> str:
    light_type = str(getattr(light_data, "type", "")).upper()

    if light_type == "SUN":
        return "directional"
    if light_type == "POINT":
        return "point"
    if light_type == "SPOT":
        return "spot"
    if light_type == "AREA":
        return "area"

    return light_type.lower()


def _collect_light_objects():
    try:
        return [obj for obj in bpy.data.objects if obj.type == "LIGHT"]
    except Exception:
        return []


def _get_intensity(light_data) -> float:
    try:
        return float(getattr(light_data, "energy", 1.0))
    except Exception:
        return 1.0


def _get_color(light_data) -> tuple[float, float, float]:
    try:
        return _safe_color(light_data.color)
    except Exception:
        return (1.0, 1.0, 1.0)


def _get_casts_shadows(light_data) -> bool:
    try:
        return bool(getattr(light_data, "use_shadow", True))
    except Exception:
        return True


def _get_emits_diffuse(light_data) -> bool:
    try:
        return float(getattr(light_data, "diffuse_factor", 1.0)) > 0.0
    except Exception:
        return True


def _get_emits_specular(light_data) -> bool:
    try:
        return float(getattr(light_data, "specular_factor", 1.0)) > 0.0
    except Exception:
        return True


def _get_enabled(obj) -> bool:
    try:
        return not bool(getattr(obj, "hide_render", False))
    except Exception:
        return True


def extract_lights() -> List[LightContext]:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    light_objects = _collect_light_objects()
    lights: List[LightContext] = []

    for obj in light_objects:
        light_data = getattr(obj, "data", None)
        if light_data is None:
            continue

        light = LightContext(
            name=obj.name,
            object_type=ObjectType.LIGHT,
            path=_get_object_path(obj),
            parent=_get_parent_path(obj),
            asset_type=AssetType.UNKNOWN,
            light_type=_get_light_type(light_data),
            intensity=_get_intensity(light_data),
            color=_get_color(light_data),
            position=_safe_vec3(obj.location),
            rotation=_safe_vec3(obj.rotation_euler),
            scale=_safe_vec3(obj.scale),
            casts_shadows=_get_casts_shadows(light_data),
            emits_diffuse=_get_emits_diffuse(light_data),
            emits_specular=_get_emits_specular(light_data),
            enabled=_get_enabled(obj),
        )

        lights.append(light)

    return lights