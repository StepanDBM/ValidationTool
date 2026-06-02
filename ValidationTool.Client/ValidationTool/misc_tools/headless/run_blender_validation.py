import bpy
import sys

script_dir = r"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool"

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from core.runner import run_pipeline
from config.validation_profile import ValidationProfile
from misc_tools.blender_adapter import extract_Blend_scene
from misc_tools.headless.fileSearchers.source_finder import get_Blender_files


SOURCE_DIR = r"C:\Users\StyopaDBM\source\repos\ValidationTool\Sourcefiles\Source_Blender"


def load_blend(file_path: str):
    bpy.ops.wm.open_mainfile(filepath=file_path)


def process_file(file_path: str):
    print(f"\n[PROCESSING BLEND] {file_path}")

    load_blend(file_path)

    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get() #forces update of evaluated data,
    #so modifiers are applied and bounding boxes are correct

    meshes = extract_Blend_scene()
    print (f"Extracted {len(meshes)} meshes from the scene")
    profile = ValidationProfile(enabled_categories=set())

    context = {"dcc": "Blender"}

    run = run_pipeline(meshes, context, profile)

    print(f"[DONE] {file_path} -> {run.run_id}")

def main():
    files = get_Blender_files(SOURCE_DIR)
    print(f"Found {len(files)} Blender files")

    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"[ERROR] {f}: {e}")


if __name__ == "__main__":
    main()