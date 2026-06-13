from core.context.SceneContext.camera_setup_context import CameraSetupContext

from misc_tools.DCC.Maya.maya_safeMultiTool import (
    _safe_get_bool,
    _safe_get_str,
)

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


_DEFAULT_CAMERA_NAMES = {"persp", "top", "front", "side"}


def _get_all_camera_shapes() -> list[str]:
    return cmds.ls(type="camera", long=True) or []


def _get_camera_transform(shape: str) -> str:
    transform = cmds.listRelatives(shape, parent=True, fullPath=True) or []
    return transform[0] if transform else ""


def _get_short_name(full_path: str) -> str:
    if not full_path:
        return ""
    return full_path.split("|")[-1]


def _is_renderable_camera(shape: str) -> bool:
    return _safe_get_bool(f"{shape}.renderable", False)


def _get_renderable_cameras(camera_shapes: list[str]) -> list[str]:
    renderable = []

    for shape in camera_shapes:
        if not _is_renderable_camera(shape):
            continue

        transform = _get_camera_transform(shape)
        if not transform:
            continue

        renderable.append(_get_short_name(transform))

    return renderable


def _get_default_cameras_present(camera_shapes: list[str]) -> list[str]:
    found = []

    for shape in camera_shapes:
        transform = _get_camera_transform(shape)
        if not transform:
            continue

        short_name = _get_short_name(transform)
        if short_name in _DEFAULT_CAMERA_NAMES:
            found.append(short_name)

    return found


def _get_active_render_camera(renderable_cameras: list[str]) -> str:
    if len(renderable_cameras) == 1:
        return renderable_cameras[0]

    # If multiple renderable cameras exist, there is no single unambiguous active render camera.
    # Keep empty so checks can flag duplicate render-camera state explicitly.
    return ""


def _get_camera_overrides_by_layer() -> dict[str, str]:
    overrides = {}

    # Legacy render layers only; render setup overrides are much more complex and renderer/version dependent.
    render_layers = cmds.ls(type="renderLayer") or []
    current_layer = _safe_get_str("editRenderLayerGlobals.currentRenderLayer", "")

    for layer in render_layers:
        if layer == "defaultRenderLayer":
            continue

        try:
            # Switch to layer temporarily to inspect layer-specific renderable cameras.
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)

            layer_camera_shapes = _get_all_camera_shapes()
            renderable = _get_renderable_cameras(layer_camera_shapes)

            if len(renderable) == 1:
                overrides[layer] = renderable[0]
            elif len(renderable) > 1:
                overrides[layer] = ",".join(renderable)

        except Exception:
            continue

    # Restore previously active layer
    try:
        if current_layer:
            cmds.editRenderLayerGlobals(currentRenderLayer=current_layer)
    except Exception:
        pass

    return overrides


def _get_expected_shot_camera(renderable_cameras: list[str]) -> str:
    # Best-effort heuristic:
    # prefer a non-default renderable camera if there is exactly one.
    non_default = [cam for cam in renderable_cameras if cam not in _DEFAULT_CAMERA_NAMES]

    if len(non_default) == 1:
        return non_default[0]

    return ""


def extract_camera_setup() -> CameraSetupContext:
    """
    Extract scene-level camera setup information from the current Maya scene.

    This includes:
    - active render camera
    - list of renderable cameras
    - default cameras present
    - render-layer camera overrides (legacy render layers)
    - duplicate/no render camera flags
    - whether a default Maya camera is used for rendering
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    camera_shapes = _get_all_camera_shapes()

    renderable_cameras = _get_renderable_cameras(camera_shapes)
    default_cameras_present = _get_default_cameras_present(camera_shapes)

    has_duplicate_render_cameras = len(renderable_cameras) > 1
    has_no_render_camera = len(renderable_cameras) == 0

    active_render_camera = _get_active_render_camera(renderable_cameras)
    camera_overrides_by_layer = _get_camera_overrides_by_layer()

    expected_shot_camera = _get_expected_shot_camera(renderable_cameras)
    uses_default_render_camera = any(cam in _DEFAULT_CAMERA_NAMES for cam in renderable_cameras)

    return CameraSetupContext(
        active_render_camera=active_render_camera,
        renderable_cameras=renderable_cameras,
        default_cameras_present=default_cameras_present,
        camera_overrides_by_layer=camera_overrides_by_layer,
        has_duplicate_render_cameras=has_duplicate_render_cameras,
        has_no_render_camera=has_no_render_camera,
        expected_shot_camera=expected_shot_camera,
        uses_default_render_camera=uses_default_render_camera,
    )