from typing import List

from core.context.baseContext import BaseContext

from misc_tools.DCC.Maya.maya_extract_meshes import extract_meshes
from misc_tools.DCC.Maya.maya_extract_cameras import extract_cameras
from misc_tools.DCC.Maya.maya_extract_lights import extract_lights

from misc_tools.DCC.Maya.maya_extract_SceneStats import extract_scene_stats
from misc_tools.DCC.Maya.maya_extract_SceneHierarchy import extract_scene_hierarchy
from misc_tools.DCC.Maya.maya_extract_SceneReferences import extract_scene_references
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
    ctx = extract_scene_setup_context()
    objects.append(ctx)
    meshes = extract_meshes()
    objects.extend(meshes)
    cameras = extract_cameras()
    objects.extend(cameras)
    lights = extract_lights()
    objects.extend(lights)
    
    objects.append(extract_scene_hierarchy())
    references = extract_scene_references()
    objects.append(references)
    objects.append(extract_scene_stats(meshes=meshes,
                                       cameras=cameras,
                                       lights=lights,
                                       references=references))

    """    
    objects.extend(extract_curves())
    objects.extend(extract_nurbs())
    """

    return objects