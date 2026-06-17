from typing import List

from core.context.baseContext import BaseContext

from misc_tools.DCC.Maya.maya_extract_meshes import extract_meshes
from misc_tools.DCC.Maya.maya_extract_cameras import extract_cameras
from misc_tools.DCC.Maya.maya_extract_lights import extract_lights
from misc_tools.DCC.Maya.maya_extract_SceneSetup.maya_extract_SSContext import extract_scene_setup_context
"""
Future extractors:
from core.dcc.maya.extract_curves import extract_curves
from core.dcc.maya.extract_nurbs import extract_nurbs
from core.dcc.maya.extract_references import extract_references"""

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def extract_maya_scene() -> List[BaseContext]:
    if cmds is None:
        raise RuntimeError("Maya API not available. Run inside Maya.")

    objects: List[BaseContext] = []
    scene_setup = extract_scene_setup_context()
    print("exctracted scene setup successfuly")
    objects.extend(extract_meshes())
    print("exctracted scene meshes successfuly")
    objects.extend(extract_cameras())
    print("exctracted scene cameras successfuly")
    objects.extend(extract_lights())
    print("exctracted scene lights successfuly")
    """    
    objects.extend(extract_curves())
    objects.extend(extract_nurbs())
    objects.extend(extract_references())
    """


    return scene_setup, objects