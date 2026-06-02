from pathlib import Path
import sys

p = Path(__file__).resolve()

# Walk upward until we find the project root
for parent in p.parents:
    if (parent / "misc_tools").exists():
        PROJECTROOT = parent
        break
else:
    raise RuntimeError("Could not locate project root")

sys.path.insert(0, str(PROJECTROOT))

print("PROJECT ROOT:", PROJECTROOT)  # debug

import maya.standalone
maya.standalone.initialize(name="python")
from misc_tools.maya_adapter import extract_meshes_from_scene
from misc_tools.headless.maya_sceneBuilder import build_test_scene
from core.runner import run_pipeline
from config.validation_profile import ValidationProfile


def main():
    build_test_scene()

    meshes = extract_meshes_from_scene()

    profile = ValidationProfile(enabled_categories=set())

    config = {}  # placeholder for future UI-driven config sync

    result = run_pipeline(meshes, config, profile)

    print("\nDONE")
    print("Run ID:", result.run_id)
    print("Assets:", len(result.assets))


if __name__ == "__main__":
    main()