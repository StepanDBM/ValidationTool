import sys
from typing import List

script_dir = r"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool"

if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.context.baseContext import BaseContext
from misc_tools.DCC.Blender.blender_extract_meshes import extract_meshes


def extract_blender_scene() -> List[BaseContext]:
    objects: List[BaseContext] = []

    objects.extend(extract_meshes())

    # Future extractors:
    # from misc_tools.DCC.Blender.blender_camera_extractor import extract_cameras
    # from misc_tools.DCC.Blender.blender_light_extractor import extract_lights
    # from misc_tools.DCC.Blender.blender_curve_extractor import extract_curves
    # from misc_tools.DCC.Blender.blender_nurbs_extractor import extract_nurbs
    # from misc_tools.DCC.Blender.blender_reference_extractor import extract_references
    #
    # objects.extend(extract_cameras())
    # objects.extend(extract_lights())
    # objects.extend(extract_curves())
    # objects.extend(extract_nurbs())
    # objects.extend(extract_references())

    return objects


def extract_Blend_scene() -> List[BaseContext]:
    return extract_blender_scene()