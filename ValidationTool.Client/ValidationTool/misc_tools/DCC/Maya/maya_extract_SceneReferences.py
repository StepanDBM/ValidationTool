from core.validation_system import ObjectType
from core.context.SceneReferenceContext import SceneReferenceContext

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


def extract_scene_references() -> SceneReferenceContext:
    refs = cmds.file(query=True, reference=True) or []

    broken = []
    unloaded = []

    for r in refs:
        try:
            if not cmds.referenceQuery(r, isLoaded=True):
                unloaded.append(r)
        except Exception:
            broken.append(r)

    return SceneReferenceContext(
        name="SceneReferences",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        references=refs,
        broken_references=broken,
        unloaded_references=unloaded
    )