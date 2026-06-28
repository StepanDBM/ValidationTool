from core.context.SceneHierarchyContext import SceneHierarchyContext
from core.validation_system import ObjectType

import bpy


def extract_scene_hierarchy() -> SceneHierarchyContext:
    all_objects = list(bpy.data.objects)

    # Root objects (no parent)
    root_objects = [
        obj.name for obj in all_objects
        if obj.parent is None
    ]

    empty_transforms = []
    groups = []
    max_depth = 0

    for obj in all_objects:
        # Compute hierarchy depth
        depth = 0
        parent = obj.parent

        while parent:
            depth += 1
            parent = parent.parent

        max_depth = max(max_depth, depth)

        # Children
        children = list(obj.children)

        # "Shapes" (data)
        has_data = obj.data is not None

        # Empty transforms (no children, no geometry)
        if not children and not has_data:
            empty_transforms.append(obj.name)

        # Groups (has children but no geometry)
        if children and not has_data:
            groups.append(obj.name)

    return SceneHierarchyContext(
        name="SceneHierarchy",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        root_objects=root_objects,
        all_transforms=[obj.name for obj in all_objects],
        empty_transforms=empty_transforms,
        groups=groups,
        max_depth=max_depth
    )