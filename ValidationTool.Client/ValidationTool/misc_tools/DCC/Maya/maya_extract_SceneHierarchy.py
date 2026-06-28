from core.validation_system import ObjectType
from core.context.SceneHierarchyContext import SceneHierarchyContext

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def extract_scene_hierarchy() -> SceneHierarchyContext:
    transforms = cmds.ls(type="transform", long=True) or []

    root_objects = [
        t for t in transforms
        if "|" not in t.strip("|")
    ]

    empty_transforms = []
    groups = []
    max_depth = 0

    for t in transforms:
        # Depth
        depth = t.count("|")
        max_depth = max(max_depth, depth)

        # Children
        children = cmds.listRelatives(t, children=True, fullPath=True) or []

        shapes = cmds.listRelatives(t, shapes=True) or []

        if not children and not shapes:
            empty_transforms.append(t)

        if children and not shapes:
            groups.append(t)

    return SceneHierarchyContext(
        name="SceneHierarchy",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        root_objects=root_objects,
        all_transforms=transforms,
        empty_transforms=empty_transforms,
        groups=groups,
        max_depth=max_depth
    )