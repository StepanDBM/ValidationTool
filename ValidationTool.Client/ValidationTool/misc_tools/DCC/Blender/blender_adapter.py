import sys
from typing import List

script_dir = r"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool"

if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.context.baseContext import BaseContext

from misc_tools.DCC.Blender.blender_extract_SceneSetup.blender_extract_SSContext import extract_scene_setup_context
from misc_tools.DCC.Blender.blender_extract_meshes import extract_meshes
from misc_tools.DCC.Blender.blender_extract_cameras import extract_cameras
from misc_tools.DCC.Blender.blender_extract_lights import extract_lights
"""
Future extractors:
from misc_tools.DCC.Blender.blender_light_extractor import extract_lights
from misc_tools.DCC.Blender.blender_curve_extractor import extract_curves
from misc_tools.DCC.Blender.blender_nurbs_extractor import extract_nurbs
from misc_tools.DCC.Blender.blender_reference_extractor import extract_references
"""

def extract_blender_scene() -> List[BaseContext]:

    objects: List[BaseContext] = []
    scene_setup = extract_scene_setup_context()
    objects.append(scene_setup)
    meshes = extract_meshes()
    objects.extend(meshes)
    cameras = extract_cameras()
    objects.extend(cameras)
    lights = extract_lights()
    objects.extend(lights)
    """
    objects.extend(extract_curves())
    objects.extend(extract_nurbs())
    objects.extend(extract_references())
    """

    return objects