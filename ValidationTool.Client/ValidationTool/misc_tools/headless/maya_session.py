import maya.standalone
maya.standalone.initialize(name="python")

from misc_tools.maya_adapter import extract_meshes_from_scene
from core.runner import run_pipeline
from config.validation_profile import ValidationProfile


def run_headless_pipeline():
    meshes = extract_meshes_from_scene()

    profile = ValidationProfile(
        name="ALL",
        enabled_categories=set()
    )

    config = {}

    return run_pipeline(meshes, config, profile)