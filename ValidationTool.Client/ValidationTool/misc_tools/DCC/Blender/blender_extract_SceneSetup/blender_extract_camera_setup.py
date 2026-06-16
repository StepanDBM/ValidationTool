from core.context.SceneContext.camera_setup_context import CameraSetupContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene
)

try:
    import bpy
except ImportError:
    bpy = None

def _get_all_camera_objects(scene) -> list:
    try:
        return [obj for obj in scene.objects if obj.type == "CAMERA"]
    except Exception:
        return []


def _get_renderable_cameras(scene, camera_objects: list) -> list[str]:
    try:
        active_camera = getattr(scene, "camera", None)
        if active_camera is not None and active_camera.type == "CAMERA":
            return [active_camera.name]
    except Exception:
        pass

    return []


def _get_default_cameras_present(camera_objects: list) -> list[str]:
    # Blender does not create Maya-style default cameras;
    # return an empty list for canonical compatibility.
    return []


def _get_active_render_camera(scene, renderable_cameras: list[str]) -> str:
    try:
        active_camera = getattr(scene, "camera", None)
        if active_camera is not None and active_camera.type == "CAMERA":
            return active_camera.name
    except Exception:
        pass

    if len(renderable_cameras) == 1:
        return renderable_cameras[0]

    return ""


def _get_camera_overrides_by_layer(scene) -> dict[str, str]:
    # Blender view layers do not expose a direct Maya-style per-render-layer camera override.
    return {}


def _get_expected_shot_camera(renderable_cameras: list[str]) -> str:
    if len(renderable_cameras) == 1:
        return renderable_cameras[0]
    return ""


def _uses_default_render_camera(renderable_cameras: list[str]) -> bool:
    # Blender has no Maya-style default render cameras.
    return False


def extract_camera_setup() -> CameraSetupContext:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    camera_objects = _get_all_camera_objects(scene)

    renderable_cameras = _get_renderable_cameras(scene, camera_objects)
    default_cameras_present = _get_default_cameras_present(camera_objects)

    has_duplicate_render_cameras = len(renderable_cameras) > 1
    has_no_render_camera = len(renderable_cameras) == 0

    active_render_camera = _get_active_render_camera(scene, renderable_cameras)
    camera_overrides_by_layer = _get_camera_overrides_by_layer(scene)

    expected_shot_camera = _get_expected_shot_camera(renderable_cameras)
    uses_default_render_camera = _uses_default_render_camera(renderable_cameras)

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