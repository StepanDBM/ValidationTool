import json
from pathlib import Path
from datetime import datetime

from core.validation_system import ValidationIssue


def build_report(issues: list[ValidationIssue]):

    from collections import Counter

    counts = Counter([i.severity.value for i in issues])

    return {
        "summary": {
            "total": len(issues),
            "errors": counts.get("ERROR", 0),
            "warnings": counts.get("WARNING", 0),
            "info": counts.get("INFO", 0)
        },
        "results": [
            {
                "asset_name": i.asset_name,
                "check_name": i.check_name,
                "severity": i.severity.value,
                "message": i.message,
                "suggestion": i.suggestion
            }
            for i in issues
        ]
    }
def write_ci_report(base_dir: str, issues: list[ValidationIssue]):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    run_folder = Path(base_dir) / timestamp
    run_folder.mkdir(parents=True, exist_ok=True)

    report = build_report(issues)

    report_path = run_folder / "validation_report.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    summary_path = run_folder / "summary.json"

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(report["summary"], f, indent=4)

    return run_folder, report