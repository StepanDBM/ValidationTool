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

import maya.standalone
maya.standalone.initialize(name="python")
import maya.cmds as cmds


from misc_tools.DCC.Maya.maya_adapter import extract_maya_scene
from core.runner import run_pipeline
from config.validation_profile import ValidationProfile

import config.absolutePaths as absPath
from fileSearchers.source_finder import get_dcc_files

from reporting.staged_json_reporter import write_session_runs
import config.dcc_list as myDCCs


def process_file(file_path: str, artist: str):

    artistFilePath = absPath.ARTISTS_DIR / file_path
    cmds.file(artistFilePath, open=True, force=True, ignoreVersion=True)

    scene_setup, objects = extract_maya_scene()
    objects = objects[1:]
    print (f"Extracted {len(objects)} meshes from the scene")
    profile = ValidationProfile(enabled_categories=set())

    context = {"dcc": "Maya", "path": file_path, "artist": artist, "scene_setup": scene_setup}

    run = run_pipeline(objects, context, profile)

    print(f"[DONE] {run.jsonPath} -> {run.summary.run_id}")
    return run

def main():

    files = get_dcc_files("maya")
    total_Mayafiles = len(files)
    index = 0

    print(f"Found {total_Mayafiles} MAYA files")

    myJsonPaths = []
    for fileInfo in files:
        try:
            file_path = fileInfo["file_path"]
            artist_log = fileInfo["artist_log"]
            
            progress = int((index/total_Mayafiles)*100)

            print(f"PROGRESS: [{progress}%]", flush = True)
            print(f"CURRENT_FILE:{file_path}", flush=True)

            index += 1
            run = process_file(file_path, artist_log)
            myJsonPaths.append(run.jsonPath)
        except Exception as e:
            print(f"[run_maya_validation_ERROR] {file_path}: {e}")

    print("PROGRESS: [100%]", flush=True)
    print("ALL FILES DONE")

    write_session_runs(myDCCs.MAYA, myJsonPaths, True)


if __name__ == "__main__":
    main()