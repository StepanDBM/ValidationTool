from core.validation_system import ObjectType
from core.context.SceneStatsContext import SceneStatsContext

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def extract_scene_stats(meshes, cameras, lights, references) -> SceneStatsContext:
    transforms = cmds.ls(type="transform") or []

    return SceneStatsContext(
        name="SceneStats",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        total_meshes=len(meshes),
        total_cameras=len(cameras),
        total_lights=len(lights),
        total_transforms=len(transforms),
        total_references=len(references.references)
    )