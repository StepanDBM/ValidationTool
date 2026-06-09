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


from misc_tools.maya_adapter import extract_Maya_scene
from core.runner import run_pipeline
from config.validation_profile import ValidationProfile

from fileSearchers.source_finder import get_MAYA_files

from reporting.staged_json_reporter import write_session_runs
import config.dcc_list as myDCCs
import config.absolutePaths as absPath



def process_file(file_path: str):
    cmds.file(file_path, open=True, force=True, ignoreVersion=True)

    meshes = extract_Maya_scene()

    profile = ValidationProfile(enabled_categories=set())

    context = {"dcc": "Maya"}

    run = run_pipeline(meshes, context, profile)

    print(f"[DONE] {file_path} -> {run.run_id}")
    
    return run


def main():
    files = get_MAYA_files(absPath.SOURCE_MAYA)

    total_MAyafiles = len(files)
    index = 0

    print(f"Found {len(files)} MAYA files")

    myJsonPaths = []
    for f in files:
        try:
            progress = int((index/total_MAyafiles)*100)

            print(f"PROGRESS: [{progress}%]", flush = True)
            print(f"CURRENT_FILE:{f}", flush=True)

            index += 1
            
            run = process_file(f)
            myJsonPaths.append(run.jsonPath)
        except Exception as e:
            print(f"[run_maya_validation_ERROR] {f}: {e}")

    print("PROGRESS: [100%]", flush=True)
    print("ALL FILES DONE")

    sessionPath = r"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\reports"
    write_session_runs(myDCCs.MAYA, myJsonPaths, absPath.REPORTS_DIR, True)


if __name__ == "__main__":
    main()