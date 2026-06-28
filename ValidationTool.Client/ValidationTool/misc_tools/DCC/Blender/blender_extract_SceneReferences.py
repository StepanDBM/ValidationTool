from core.validation_system import ObjectType
from core.context.SceneReferenceContext import SceneReferenceContext

import bpy


def extract_scene_references() -> SceneReferenceContext:
    references = []
    broken = []
    unloaded = []

    # All external libraries (linked .blend files)
    libraries = bpy.data.libraries

    for lib in libraries:
        filepath = lib.filepath

        references.append(filepath)

        # Check if file exists → broken reference
        try:
            import os
            if not os.path.exists(bpy.path.abspath(filepath)):
                broken.append(filepath)
        except Exception:
            broken.append(filepath)

        # In Blender, libraries are either available or not
        # If path exists but nothing is loaded, we treat as "unloaded"
        # (best-effort approximation)
        if not lib.users_id:
            unloaded.append(filepath)

    return SceneReferenceContext(
        name="SceneReferences",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        references=references,
        broken_references=broken,
        unloaded_references=unloaded
    )