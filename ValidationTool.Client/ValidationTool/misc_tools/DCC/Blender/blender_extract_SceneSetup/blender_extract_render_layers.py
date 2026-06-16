import re

from core.context.SceneContext.render_layer_context import RenderLayerContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene
)

try:
    import bpy
except ImportError:
    bpy = None


_VALID_LAYER_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def _get_view_layers(scene) -> list:
    try:
        return list(scene.view_layers)
    except Exception:
        return []


def _get_active_view_layer_name() -> str:
    try:
        if bpy.context.view_layer:
            return bpy.context.view_layer.name
    except Exception:
        pass
    return ""


def _is_layer_required(view_layer_name: str) -> bool:
    return view_layer_name == "ViewLayer"


def _has_valid_name(view_layer_name: str) -> bool:
    return bool(_VALID_LAYER_NAME_PATTERN.match(view_layer_name))


def _get_scene_member_count(scene) -> int:
    try:
        return len(scene.objects)
    except Exception:
        return 0


def _get_renderable_camera(scene) -> str:
    try:
        cam = getattr(scene, "camera", None)
        if cam is not None and cam.type == "CAMERA":
            return cam.name
    except Exception:
        pass
    return ""


def _get_material_override(view_layer) -> str:
    # Blender does not expose a Maya-style per-view-layer material override in a generic/simple way.
    return ""


def _iter_layer_collections(layer_collection):
    yield layer_collection
    try:
        for child in layer_collection.children:
            yield from _iter_layer_collections(child)
    except Exception:
        return


def _get_collection_overrides(view_layer) -> list[str]:
    result = []

    try:
        root = view_layer.layer_collection
        for layer_col in _iter_layer_collections(root):
            name = getattr(layer_col.collection, "name", "")
            if not name:
                continue

            # Treat non-default visibility/exclusion flags as collection-level overrides.
            exclude = bool(getattr(layer_col, "exclude", False))
            holdout = bool(getattr(layer_col, "holdout", False))
            indirect_only = bool(getattr(layer_col, "indirect_only", False))

            if exclude or holdout or indirect_only:
                result.append(name)
    except Exception:
        pass

    return result


def _get_light_overrides(view_layer) -> list[str]:
    # Blender view layers do not expose Maya-style explicit light overrides generically.
    return []


def _get_object_overrides(view_layer) -> list[str]:
    # Blender view layers do not expose Maya-style object override lists generically.
    return []


def _is_layer_renderable(view_layer) -> bool:
    # Blender view layers are generally considered renderable if they exist.
    return True


def extract_render_layers() -> list[RenderLayerContext]:
    """
    Extract Blender View Layers and map them into the shared RenderLayerContext.
    """

    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    view_layers = _get_view_layers(scene)
    active_view_layer_name = _get_active_view_layer_name()
    scene_member_count = _get_scene_member_count(scene)
    active_camera = _get_renderable_camera(scene)

    contexts: list[RenderLayerContext] = []

    for view_layer in view_layers:
        name = getattr(view_layer, "name", "")

        collection_overrides = _get_collection_overrides(view_layer)
        light_overrides = _get_light_overrides(view_layer)
        object_overrides = _get_object_overrides(view_layer)

        context = RenderLayerContext(
            name=name,
            enabled=True,
            renderable=_is_layer_renderable(view_layer),
            is_active=(name == active_view_layer_name),
            camera_override=active_camera,
            material_override=_get_material_override(view_layer),
            light_overrides=light_overrides,
            object_overrides=object_overrides,
            collection_overrides=collection_overrides,
            has_members=scene_member_count > 0,
            member_count=scene_member_count,
            has_valid_name=_has_valid_name(name),
            is_required=_is_layer_required(name),
        )

        contexts.append(context)

    return contexts