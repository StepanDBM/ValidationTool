from core.context.SceneContext.color_management_context import ColorManagementContext
from misc_tools.DCC.Blender.blender_safeMultiTool import (
    _get_scene,
    _safe_str,
    _safe_float
)

import os

try:
    import bpy
except ImportError:
    bpy = None


def _get_view_transform(scene) -> str:
    try:
        return _safe_str(scene.view_settings.view_transform, "")
    except Exception:
        return ""


def _get_display_device(scene) -> str:
    try:
        return _safe_str(scene.display_settings.display_device, "")
    except Exception:
        return ""


def _get_render_color_space(scene) -> str:
    try:
        sequencer_settings = getattr(scene, "sequencer_colorspace_settings", None)
        if sequencer_settings is not None:
            return _safe_str(getattr(sequencer_settings, "name", ""), "")
    except Exception:
        pass

    return ""


def _get_texture_color_management_mode(scene) -> str:
    return ""


def _get_ocio_config() -> str:
    try:
        ocio_env = os.environ.get("OCIO", "")
        if ocio_env:
            return ocio_env
    except Exception:
        pass

    return "Blender Built-in OCIO"


def _get_linear_workflow_enabled(scene) -> bool:
    return True


def _get_aces_enabled(view_transform: str, render_color_space: str, ocio_config: str) -> bool:
    merged = f"{view_transform} {render_color_space} {ocio_config}".upper()
    return "ACES" in merged


def _get_gamma(scene) -> float:
    try:
        return _safe_float(scene.view_settings.gamma, 1.0)
    except Exception:
        return 1.0


def _get_exposure(scene) -> float:
    try:
        return _safe_float(scene.view_settings.exposure, 0.0)
    except Exception:
        return 0.0


def _get_look(scene) -> str:
    try:
        return _safe_str(scene.view_settings.look, "")
    except Exception:
        return ""


def extract_color_management() -> ColorManagementContext:
    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene = _get_scene()
    if scene is None:
        raise RuntimeError("No Blender scene available.")

    view_transform = _get_view_transform(scene)
    display_device = _get_display_device(scene)
    render_color_space = _get_render_color_space(scene)

    texture_color_management_mode = _get_texture_color_management_mode(scene)
    ocio_config = _get_ocio_config()

    linear_workflow_enabled = _get_linear_workflow_enabled(scene)
    aces_enabled = _get_aces_enabled(view_transform, render_color_space, ocio_config)

    gamma = _get_gamma(scene)
    exposure = _get_exposure(scene)
    look = _get_look(scene)

    return ColorManagementContext(
        view_transform=view_transform,
        display_device=display_device,
        render_color_space=render_color_space,
        texture_color_management_mode=texture_color_management_mode,
        ocio_config=ocio_config,
        linear_workflow_enabled=linear_workflow_enabled,
        aces_enabled=aces_enabled,
        gamma=gamma,
        exposure=exposure,
        look=look,
    )
