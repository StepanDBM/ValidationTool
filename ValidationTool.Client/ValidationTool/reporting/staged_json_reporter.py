import json
from typing import Dict, Any
import config.exec_stages as excS
from pathlib import Path


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
            "originFile": issue.originFile,
            "asset_name": issue.asset_name,
            "check_name": issue.check_name,
            "stage": issue.stage,
            "timestamp": str(issue.timestamp),
            "severity": issue.severity.value,
            "message": issue.message,
            "suggestion": issue.suggestion
        }
        mIssues.append(issue_obj)

    return {
        "summary": summary,
        "issues": mIssues
    }

def write_json(run, folder_path: Path, pretty: bool = True):
    
    data = export_validation_run(run)
    
    folder_path.mkdir(parents=True, exist_ok=True)
    
    run_folder = folder_path / f"{run.summary.dcc}_runID_{run.summary.run_id}"
    
    run_folder.mkdir(parents=True, exist_ok=True)

    report_file = run_folder / "validation_report.json"
    
    with report_file.open("w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    return str(report_file)

def write_session_runs(mydcc, sessionRuns, folder_path: Path, pretty: bool = True):

    data = {
        "dcc": mydcc,
        "runs": sessionRuns
    }
    folder_path.mkdir(parents=True, exist_ok=True)
    report_file = folder_path / f"{mydcc}_reports.json"
    
    try:
        with report_file.open("w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"[write_session_runs: ERROR - {f} as {e}]")