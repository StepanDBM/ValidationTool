import os

from core.context.baseContext import BaseContext
from core.context.SceneContext.SceneSetupContext import SceneSetupContext
from core.validation_system import ObjectType

from dataclasses import asdict, is_dataclass
from pprint import pformat

from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_render_settings import extract_render_settings
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_output_settings import extract_output_settings
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_sampling_settings import extract_sampling_settings
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_ray_depth_settings import extract_ray_depth_settings
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_color_management import extract_color_management
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_camera_setup import extract_camera_setup
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_render_layers import extract_render_layers
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_aovs import extract_aovs

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None



def pretty_print_context(title: str, obj):
    print(f"\n[{title}]")
    print("-" * (len(title) + 2))

    if is_dataclass(obj):
        print(pformat(asdict(obj), sort_dicts=False, width=120))
    else:
        print(pformat(obj, sort_dicts=False, width=120))



def _get_scene_path() -> str:
    try:
        return cmds.file(query=True, sceneName=True) or ""
    except Exception:
        return ""


def _get_scene_name(scene_path: str) -> str:
    if not scene_path:
        return "untitled_scene"
    return os.path.splitext(os.path.basename(scene_path))[0]


def _get_project_path() -> str:
    try:
        return cmds.workspace(query=True, rootDirectory=True) or ""
    except Exception:
        return ""


def _get_dcc_version() -> str:
    try:
        return str(cmds.about(version=True))
    except Exception:
        return ""


def extract_scene_setup_context() -> SceneSetupContext:

    """
    Extracts the full scene-level setup configuration from the current Maya scene.

    Returns:
        SceneSetupContext: Aggregated scene setup data including render settings,
        output settings, sampling, ray depth, color management, camera setup,
        render layers, and AOVs.

    Raises:
        RuntimeError: If Maya commands are not available.
    """

    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    scene_path = _get_scene_path()
    scene_name = _get_scene_name(scene_path)
    project_path = _get_project_path()

    render_settings = extract_render_settings()
    #pretty_print_context("[RENDER SETTINGS]: ", render_settings)
    output_settings = extract_output_settings()
    #pretty_print_context("[OUTPUT SETTINGS]: ", output_settings)
    sampling_settings = extract_sampling_settings()
    #pretty_print_context("[SAMPLING SETTINGS]: ", sampling_settings)
    ray_depth_settings = extract_ray_depth_settings()
    #pretty_print_context("[RAY DEPTH SETTINGS]: ", ray_depth_settings)
    color_management = extract_color_management()
    #pretty_print_context("[COLORM ANAGEMENT]: ", color_management)
    camera_setup = extract_camera_setup()
    #pretty_print_context("[CAMERA SETUP]: ", camera_setup)
    render_layers = extract_render_layers()
    #pretty_print_context("[RENDER LAYERS]: ", render_layers)
    aovs = extract_aovs()
    #pretty_print_context("[AOVs]: ", aovs)

    scene_setup = SceneSetupContext(
        name=scene_name,
        object_type=ObjectType.SCENE,
        path=scene_path,
        parent="",

        scene_name=scene_name,
        scene_path=scene_path,
        project_path=project_path,

        dcc_name="Maya",
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