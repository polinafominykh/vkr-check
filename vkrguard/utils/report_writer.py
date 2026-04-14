import json
from pathlib import Path
from vkrguard.schemes.results import EvaluationReport


def save_report_to_json(report: EvaluationReport, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)