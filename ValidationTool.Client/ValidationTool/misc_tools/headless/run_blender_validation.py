from pathlib import Path
import sys

p = Path(__file__).resolve()

# Walk upward until we find the project root
for parent in p.parents:
    if (parent / ".validation_tool").exists():
        PROJECTROOT = parent
        break
else:
    raise RuntimeError("Could not locate project root")

sys.path.insert(0, str(PROJECTROOT))

import bpy

from core.runner import run_pipeline
from config.validation_profile import ValidationProfile
from misc_tools.blender_adapter import extract_Blend_scene
from misc_tools.headless.fileSearchers.source_finder import get_Blender_files
from reporting.staged_json_reporter import write_session_runs
import config.dcc_list as myDCCs
import config.absolutePaths as absPath



def load_blend(file_path: str):
    bpy.ops.wm.open_mainfile(filepath=file_path)


def process_file(file_path: str):

    load_blend(file_path)

    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get() #forces update of evaluated data,
    #so modifiers are applied and bounding boxes are correct

    meshes = extract_Blend_scene()
    print (f"Extracted {len(meshes)} meshes from the scene")
    profile = ValidationProfile(enabled_categories=set())

    context = {"dcc": "Blender", "path": "file_path"}

    run = run_pipeline(meshes, context, profile)
    
    print(f"[DONE] {file_path} -> {run.summary.run_id}")
    return run

def main():
    files = get_Blender_files(absPath.SOURCE_BLENDER)

    total_blendFiles = len(files)
    index = 0
    
    print(f"Found {total_blendFiles} .BLENDs")

    myJsonPaths = []
    for f in files:
        try:
            progress = int((index/total_blendFiles)*100)

            print(f"PROGRESS: [{progress}%]", flush = True)
            print(f"\n[PROCESSING .BLEND]{f}", flush=True)

            index += 1

            run = process_file(f)
            myJsonPaths.append(run.jsonPath)
        except Exception as e:
            print(f"[run_blender_validation_ERROR] {f}: {e}")

    print("PROGRESS: [100%]", flush=True)
    print("ALL FILES DONE")
    
    write_session_runs(myDCCs.BLENDER, myJsonPaths, absPath.REPORTS_DIR, True)


if __name__ == "__main__":
    main()