from pathlib import Path
import sys

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

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
#from config.validation_profile import ValidationProfile
from misc_tools.DCC.Blender.blender_adapter import extract_blender_scene
from misc_tools.headless.fileSearchers.source_finder import get_dcc_files
from reporting.staged_json_reporter import write_session_runs
from reporting.config_loader import ConfigLoader
import config.dcc_list as myDCCs
import config.absolutePaths as absPath



def load_blend(file_path: str):
    bpy.ops.wm.open_mainfile(filepath=str(file_path))


def process_file(file_path: str, artist: str):
    artistFilePath = absPath.ARTISTS_DIR / file_path
    load_blend(artistFilePath)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get() #forces update of evaluated data,
    #so modifiers are applied and bounding boxes are correct
    scene_setup, objects = extract_blender_scene()
    
    loader = ConfigLoader(absPath.CONFIG_DIR)
    profile = loader.load_profile()
    context = {"headless":1, "dcc": "Blender", "path": file_path, "artist": artist, "scene_setup": scene_setup}

    run = run_pipeline(objects, context, profile)
    
    print(f"[DONE] {run.jsonPath} -> {run.summary.run_id}", flush=True)
    return run

def main():
    files = get_dcc_files("blender")
    total_blendFiles = len(files)
    index = 0
    
    print(f"Found {total_blendFiles} Blender files.")

    myJsonPaths = []
    for fileInfo in files:
        try:
            file_path = fileInfo["file_path"]
            artist_log = fileInfo["artist_log"]
            
            progress = int((index/total_blendFiles)*100)

            print(f"PROGRESS: [{progress}%]", flush=True)
            print(f"CURRENT FILE: {file_path}", flush=True)

            index += 1

            run = process_file(file_path, artist_log)
            myJsonPaths.append(run.jsonPath)
        except Exception as e:
            print(f"[run_blender_validation_ERROR] {file_path}: {e}", flush=True)

    print("PROGRESS: [100%]", flush=True)
    print("ALL FILES DONE", flush=True)
    write_session_runs(myDCCs.BLENDER, myJsonPaths, True)


if __name__ == "__main__":
    main()