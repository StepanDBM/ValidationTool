from pathlib import Path
import sys

import maya.standalone
maya.standalone.initialize(name="python")
import maya.cmds as cmds

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

from misc_tools.maya_adapter import extract_meshes_from_scene
from core.runner import run_pipeline
from config.validation_profile import ValidationProfile

from fileSearchers.source_finder import get_MAYA_files


SOURCE_DIR = r"C:\Users\StyopaDBM\source\repos\ValidationTool\Sourcefiles\Source_Maya"


def process_file(file_path: str):
    print(f"\n[PROCESSING] {file_path}")
    cmds.file(file_path, open=True, force=True, ignoreVersion=True)

    meshes = extract_meshes_from_scene()

    profile = ValidationProfile(enabled_categories=set())

    config = {}

    result = run_pipeline(meshes, config, profile)

    print(f"[DONE] {file_path} -> {result.run_id}")


def main():
    files = get_MAYA_files(SOURCE_DIR)

    print(f"Found {len(files)} Maya files")

    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"[ERROR] {f}: {e}")


if __name__ == "__main__":
    main()