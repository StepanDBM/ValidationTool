import re

from core.context.SceneContext.render_layer_context import RenderLayerContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_bool,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_VALID_LAYER_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

_MAYA_LIGHT_NODE_TYPES = {
    "ambientLight",
    "directionalLight",
    "pointLight",
    "spotLight",
    "areaLight",
    "volumeLight",
    "aiAreaLight",
    "aiSkyDomeLight",
    "aiPhotometricLight",
    "aiMeshLight",
}


def _get_short_name(full_path: str) -> str:
    if not full_path:
        return ""
    return full_path.split("|")[-1]


def _get_all_render_layers() -> list[str]:
    return cmds.ls(type="renderLayer") or []


def _get_current_render_layer() -> str:
    return _safe_get_str("editRenderLayerGlobals.currentRenderLayer", "defaultRenderLayer")


def _is_layer_renderable(layer: str) -> bool:
    return _safe_get_bool(f"{layer}.renderable", False)


def _is_layer_required(layer: str) -> bool:
    return layer == "defaultRenderLayer"


def _has_valid_name(layer: str) -> bool:
    return bool(_VALID_LAYER_NAME_PATTERN.match(layer))


def _get_layer_members(layer: str) -> list[str]:
    try:
        members = cmds.editRenderLayerMembers(layer, query=True, fullNames=True) or []
        return members
    except Exception:
        return []


def _get_renderable_camera_for_current_layer() -> str:
    camera_shapes = cmds.ls(type="camera", long=True) or []

    renderable = []
    for shape in camera_shapes:
        try:
            if not _safe_get_bool(f"{shape}.renderable", False):
                continue

            transform = cmds.listRelatives(shape, parent=True, fullPath=True) or []
            if not transform:
                continue

            renderable.append(_get_short_name(transform[0]))
        except Exception:
            continue

    if len(renderable) == 1:
        return renderable[0]

    if len(renderable) > 1:
        return ",".join(renderable)

    return ""


def _get_material_override(layer: str) -> str:
    # Best-effort legacy render layer material override detection.
    # Maya can implement material overrides in different ways depending on setup,
    # so this stays conservative.
    try:
        adjustments = cmds.editRenderLayerAdjustment(layer, query=True) or []
    except Exception:
        return ""

    for adj in adjustments:
        node_name = adj.split(".")[0]
        try:
            node_type = cmds.nodeType(node_name)
        except Exception:
            continue

        if node_type in {"shadingEngine", "lambert", "blinn", "phong", "aiStandardSurface"}:
            return _get_short_name(node_name)

    return ""


def _get_adjustments(layer: str) -> list[str]:
    try:
        return cmds.editRenderLayerAdjustment(layer, query=True) or []
    except Exception:
        return []


def _split_adjustments(adjustments: list[str]) -> tuple[list[str], list[str]]:
    light_overrides = []
    object_overrides = []

    seen_lights = set()
    seen_objects = set()

    for adj in adjustments:
        node_name = adj.split(".")[0]

        try:
            node_type = cmds.nodeType(node_name)
        except Exception:
            continue

        short_name = _get_short_name(node_name)

        if node_type in _MAYA_LIGHT_NODE_TYPES:
            if short_name not in seen_lights:
                seen_lights.add(short_name)
                light_overrides.append(short_name)
            continue

        if node_type == "transform":
            if short_name not in seen_objects:
                seen_objects.add(short_name)
                object_overrides.append(short_name)
            continue

        # Shapes / meshes / cameras / anything scene-object-like
        try:
            if cmds.objectType(node_name, isAType="shape"):
                parents = cmds.listRelatives(node_name, parent=True, fullPath=True) or []
                if parents:
                    short_name = _get_short_name(parents[0])

            if short_name not in seen_objects:
                seen_objects.add(short_name)
                object_overrides.append(short_name)
        except Exception:
            continue

    return light_overrides, object_overrides


def extract_render_layers() -> list[RenderLayerContext]:
    """
    Extract legacy Maya render-layer configuration from the current scene.

    Returns:
        list[RenderLayerContext]: One context per render layer.

    Notes:
        - This targets Maya legacy render layers.
        - Render Setup overrides are more complex and are not fully covered here.
        - camera_override is determined by temporarily switching the active layer
          and reading renderable cameras in that layer state.
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    layers = _get_all_render_layers()
    contexts: list[RenderLayerContext] = []

    current_layer = _get_current_render_layer()

    for layer in layers:
        try:
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)
        except Exception:
            pass

        members = _get_layer_members(layer)
        member_count = len(members)
        has_members = member_count > 0

        adjustments = _get_adjustments(layer)
        light_overrides, object_overrides = _split_adjustments(adjustments)

        context = RenderLayerContext(
            name=layer,
            enabled=True,
            renderable=_is_layer_renderable(layer),
            is_active=(layer == current_layer),
            camera_override=_get_renderable_camera_for_current_layer(),
            material_override=_get_material_override(layer),
            light_overrides=light_overrides,
            object_overrides=object_overrides,
            collection_overrides=[],  # Maya legacy render layers do not have Blender-style collections
            has_members=has_members,
            member_count=member_count,
            has_valid_name=_has_valid_name(layer),
            is_required=_is_layer_required(layer),
        )

        contexts.append(context)

    try:
        cmds.editRenderLayerGlobals(currentRenderLayer=current_layer)
    except Exception:
        pass

    return contexts