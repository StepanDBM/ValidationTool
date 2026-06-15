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
from misc_tools.DCC.Blender.blender_adapter import extract_Blend_scene
from misc_tools.headless.fileSearchers.source_finder import get_dcc_files
from reporting.staged_json_reporter import write_session_runs
import config.dcc_list as myDCCs
import config.absolutePaths as absPath



def load_blend(file_path: str):
    bpy.ops.wm.open_mainfile(filepath=file_path)


def process_file(file_path: str, artist: str):
    load_blend(file_path)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get() #forces update of evaluated data,
    #so modifiers are applied and bounding boxes are correct

    objects = extract_Blend_scene()
    print (f"Extracted {len(objects)} meshes from the scene")
    profile = ValidationProfile(enabled_categories=set())

    context = {"dcc": "Blender", "path": file_path, "artist": artist}

    run = run_pipeline(objects, context, profile)
    
    print(f"[DONE] {file_path} -> {run.summary.run_id}")
    return run

def main():
    files = get_dcc_files(absPath.ARTISTS_DIR, "blender")

    total_blendFiles = len(files)
    index = 0
    
    print(f"Found {total_blendFiles} .BLENDs")

    myJsonPaths = []
    for fileInfo in files:
        try:
            file_path = fileInfo["file_path"]
            artist_log = fileInfo["artist_log"]
            
            progress = int((index/total_blendFiles)*100)

            print(f"PROGRESS: [{progress}%]", flush = True)
            print(f"\n[PROCESSING .BLEND]{file_path}", flush=True)

            index += 1

            run = process_file(file_path, artist_log)
            myJsonPaths.append(run.jsonPath)
        except Exception as e:
            print(f"[run_blender_validation_ERROR] {file_path}: {e}")

    print("PROGRESS: [100%]", flush=True)
    print("ALL FILES DONE")
    
    write_session_runs(myDCCs.BLENDER, myJsonPaths, absPath.REPORTS_DIR, True)


if __name__ == "__main__":
    main()