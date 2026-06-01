import json
from typing import Dict, Any
import config.exec_stages as excS


def export_validation_run(run) -> Dict[str, Any]:
    """
    Converts ValidationRun into structured JSON dict.
    Keeps stage order, asset grouping, and issue hierarchy.
    """
    summary = {
        "run_id": run.run_id,
        "timestamp": str(run.timestamp),
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


from pathlib import Path
from datetime import datetime
import json


from pathlib import Path
from datetime import datetime
import json


from pathlib import Path
from datetime import datetime
import json


def write_json(run, folder_path: str, pretty: bool = True):
    """
    Writes ValidationRun into a timestamped folder under folder_path.
    folder_path MUST be a directory.
    """

    data = export_validation_run(run)

    # Ensure base directory exists
    base_dir = Path(folder_path)
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create timestamped run folder
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_folder = base_dir / timestamp
    run_folder.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # MAIN REPORT
    # -------------------------
    report_file = run_folder / "validation_report.json"

    with report_file.open("w", encoding="utf-8") as f:
        if pretty:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    # -------------------------
    # SUMMARY
    # -------------------------
    summary_file = run_folder / "summary.json"

    summary = {
        "run_id": run.run_id,
        "timestamp": str(run.timestamp),
        "total_assets": len(run.assets),
        "total_issues": run.summary.total_issues,
        "errors": run.summary.errors,
        "warnings": run.summary.warnings,
        "info": run.summary.infos
    }

    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4 if pretty else None, ensure_ascii=False)