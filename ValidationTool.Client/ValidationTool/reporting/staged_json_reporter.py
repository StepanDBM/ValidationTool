import json
from typing import Dict, Any
from pathlib import Path

import json
from typing import Dict, Any
from pathlib import Path
from dataclasses import is_dataclass, asdict
from datetime import datetime

import json
from pathlib import Path
from dataclasses import is_dataclass, asdict
from datetime import datetime
from enum import Enum
import config.absolutePaths as absPath


def _to_json_safe(value):
    """
    Recursively converts dataclasses and common Python objects
    into JSON-serializable structures.
    """
    if value is None:
        return None

    if is_dataclass(value):
        return {
            k: _to_json_safe(v)
            for k, v in asdict(value).items()
        }

    if isinstance(value, dict):
        return {
            str(k): _to_json_safe(v)
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [_to_json_safe(v) for v in value]

    if isinstance(value, tuple):
        return [_to_json_safe(v) for v in value]

    if isinstance(value, datetime):
        return str(value)

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, Enum):
        return value.value if hasattr(value, "value") else str(value)

    return value


def export_validation_run(run) -> Dict[str, Any]:
    
    summary = {
        "run_id": run.summary.run_id,
        "timestamp": str(run.summary.timestamp),
        "dcc": run.summary.dcc,

        "total_assets": run.summary.total_objects,
        "total_issues": run.summary.total_issues,
        "errors": run.summary.errors,
        "warnings": run.summary.warnings,
        "infos": run.summary.infos
    }
    
    mIssues = []
    for issue in run.issues:

        issue_obj = {
            "artist": issue.artist,
            "dcc": issue.dcc,
            "origin_file": _to_json_safe(issue.origin_file),
            "object_name": issue.object_name,
            "check_name": issue.check_name,
            "stage": issue.stage,
            "timestamp": str(issue.timestamp),
            "severity": issue.severity.value,
            "message": issue.message,
            "suggestion": issue.suggestion,
            "fix_mode":issue.fix_mode
        }
        mIssues.append(issue_obj)

    scene_setup = None
    if hasattr(run, "scene_setup_context"):
        scene_setup = _to_json_safe(run.scene_setup_context)
    elif hasattr(run, "scene_setup"):
        scene_setup = _to_json_safe(run.scene_setup)

    return {
        "summary": summary,
        "scene_setup": scene_setup,
        "issues": mIssues
    }

def write_json(run, pretty: bool = True):
    
    data = export_validation_run(run)
    
    
    run_folder = f"{run.summary.dcc}_runID_{run.summary.run_id}"
    
    folder_path = absPath.REPORTS_DIR
    folder_path.mkdir(parents=True, exist_ok=True)
    folder_path = folder_path / run_folder
    folder_path.mkdir(parents=True, exist_ok=True)

    report_file = folder_path / "validation_report.json"
    
    with report_file.open("w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    return run_folder + "/validation_report.json"

def write_session_runs(mydcc, sessionRuns, pretty: bool = True):

    data = {
        "dcc": mydcc,
        "runs": sessionRuns
    }
        
    report_file = absPath.REPORTS_DIR / f"{mydcc}_reports.json"
    
    try:
        with report_file.open("w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"[write_session_runs: ERROR - {f} as {e}]")