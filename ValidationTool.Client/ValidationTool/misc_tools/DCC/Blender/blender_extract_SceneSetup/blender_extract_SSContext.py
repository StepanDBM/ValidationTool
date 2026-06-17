import os

from core.context.SceneContext.SceneSetupContext import SceneSetupContext
from core.validation_system import ObjectType

from dataclasses import asdict, is_dataclass
from pprint import pformat

from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_render_settings import extract_render_settings
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_output_settings import extract_output_settings
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_sampling_settings import extract_sampling_settings
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_ray_depth_settings import extract_ray_depth_settings
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_color_management import extract_color_management
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_camera_setup import extract_camera_setup
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_render_layers import extract_render_layers
from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_aovs import extract_aovs

try:
    import bpy
except ImportError:
    bpy = None

from misc_tools.DCC.Maya.maya_safeMultiTool import _pretty_print_context

def _get_scene_path() -> str:
    try:
        return bpy.data.filepath or ""
    except Exception:
        return ""


def _get_scene_name(scene_path: str) -> str:
    if not scene_path:
        return "untitled_scene"
    return os.path.splitext(os.path.basename(scene_path))[0]


def _get_project_path(scene_path: str) -> str:
    try:
        if scene_path:
            return os.path.dirname(scene_path)
        return bpy.path.abspath("//") or ""
    except Exception:
        return ""


def _get_dcc_version() -> str:
    try:
        return bpy.app.version_string
    except Exception:
        return ""


def extract_scene_setup_context() -> SceneSetupContext:
    """
    Extracts the full scene-level setup configuration from the current Blender scene.

    Returns:
        SceneSetupContext: Aggregated scene setup data including render settings,
        output settings, sampling, ray depth, color management, camera setup,
        render layers, and AOVs.

    Raises:
        RuntimeError: If Blender API is not available.
    """

    if bpy is None:
        raise RuntimeError("Blender API not available. Run inside Blender.")

    scene_path = _get_scene_path()
    scene_name = _get_scene_name(scene_path)
    project_path = _get_project_path(scene_path)
    render_settings = extract_render_settings()
    #_pretty_print_context("RENDER SETTINGS", render_settings)
    output_settings = extract_output_settings()
    #_pretty_print_context("OUTPUT SETTINGS", output_settings)
    sampling_settings = extract_sampling_settings()
    #_pretty_print_context("SAMPLING SETTINGS", sampling_settings)
    ray_depth_settings = extract_ray_depth_settings()
    #_pretty_print_context("RAY DEPTH SETTINGS", ray_depth_settings)
    color_management = extract_color_management()
    #_pretty_print_context("COLOR MANAGEMENT", color_management)
    camera_setup = extract_camera_setup()
    #_pretty_print_context("CAMERA SETUP", camera_setup)
    render_layers = extract_render_layers()
    #_pretty_print_context("RENDER LAYERS", render_layers)
    aovs = extract_aovs()
    #_pretty_print_context("AOVs", aovs)

    scene_setup = SceneSetupContext(
        name=scene_name,
        object_type=ObjectType.SCENE,
        path=scene_path,
        parent="",

        scene_name=scene_name,
        project_path=project_path,

        dcc_name="Blender",
        dcc_version=_get_dcc_version(),

        render_settings=render_settings,
        output_settings=output_settings,
        sampling_settings=sampling_settings,
        ray_depth_settings=ray_depth_settings,
        color_management=color_management,
        camera_setup=camera_setup,

        render_layers=render_layers,
        aovs=aovs
    )

    return scene_setup