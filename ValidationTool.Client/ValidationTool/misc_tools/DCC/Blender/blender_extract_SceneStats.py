from core.validation_system import ObjectType
from core.context.SceneStatsContext import SceneStatsContext

import bpy


def extract_scene_stats(meshes, cameras, lights, references) -> SceneStatsContext:
    # Use scene objects (not all datablocks)
    scene_objects = bpy.context.scene.objects

    # Blender objects already represent transforms
    total_transforms = len(scene_objects)

    return SceneStatsContext(
        name="SceneStats",
        object_type=ObjectType.SCENE,
        path="",
        parent="",

        total_meshes=len(meshes),
        total_cameras=len(cameras),
        total_lights=len(lights),
        total_transforms=total_transforms,
        total_references=len(references.references)
    )