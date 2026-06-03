import json
from typing import Dict, Any
import config.exec_stages as excS
from pathlib import Path


def export_validation_run(run) -> Dict[str, Any]:
    
    summary = {
        "run_id": run.run_id,
        "timestamp": str(run.timestamp),
        "dcc": run.dcc,

        "total_assets": len(run.assets),
        "total_issues": run.summary.total_issues,
        "errors": run.summary.errors,
        "warnings": run.summary.warnings,
        "info": run.summary.infos
    }

    assets_json = []

    for asset in run.assets:

        asset_obj = {
            "asset_name": asset.asset_name,
            "has_errors": asset.has_errors,
            "total_issues": asset.total_issues,
            "stages": []
        }

        # enforce stage ordering (critical for UI consistency)
        stage_map = {s.stage: s for s in asset.stages}

        for stage in excS.EXECUTION_STAGES:

            stage_data = stage_map.get(stage)

            if not stage_data:
                continue

            stage_obj = {
                "stage": stage,
                "has_errors": stage_data.has_errors,
                "execution_time": stage_data.execution_time,
                "issues": []
            }

            for issue in stage_data.issues:
                stage_obj["issues"].append({
                    "asset_name": issue.asset_name,
                    "check_name": issue.check_name,
                    "severity": issue.severity.value,
                    "message": issue.message,
                    "suggestion": getattr(issue, "suggestion", "")
                })

            asset_obj["stages"].append(stage_obj)

        assets_json.append(asset_obj)

    return {
        "summary": summary,
        "assets": assets_json
    }

def write_json(run, folder_path: Path, pretty: bool = True):

    data = export_validation_run(run)

    folder_path.mkdir(parents=True, exist_ok=True)
    
    run_folder = folder_path / f"{run.dcc}_runID_{run.run_id}"
    
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
    print(data)
    folder_path.mkdir(parents=True, exist_ok=True)
    report_file = folder_path / f"{mydcc}_reports.json"
    print (report_file)
    try:

        with report_file.open("w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"[write_session_runs: ERROR - {f} as {e}]")