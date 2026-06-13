from typing import List

from core.context.baseContext import BaseContext
from misc_tools.DCC.Maya.maya_extract_meshes import extract_meshes
from misc_tools.DCC.Maya.maya_extract_cameras import extract_cameras
from misc_tools.DCC.Maya.maya_extract_lights import extract_lights
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

    objects.extend(extract_meshes())
    objects.extend(extract_cameras())
    objects.extend(extract_lights())
    """    
    objects.extend(extract_curves())
    objects.extend(extract_nurbs())
    objects.extend(extract_references())
    """


    return objects