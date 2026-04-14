import json
from pathlib import Path
from typing import List

from vkrguard.schemes.results import EvaluationReport


def save_batch_summary(reports: List[EvaluationReport], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(reports)
    total_checks = 0
    total_passed = 0

    files_summary = []

    for report in reports:
        summary = report.summary or {}
        passed_checks = summary.get("passed_checks", 0)
        checks_count = summary.get("total_checks", 0)
        score = summary.get("score", 0.0)
        status = summary.get("overall_status", "unknown")

        total_checks += checks_count
        total_passed += passed_checks

        files_summary.append(
            {
                "file_path": report.file_path,
                "found_sections": report.found_sections,
                "score": score,
                "overall_status": status,
                "passed_checks": passed_checks,
                "total_checks": checks_count,
            }
        )

    overall_score = round((total_passed / total_checks) * 100, 2) if total_checks else 0.0

    data = {
        "total_files": total_files,
        "total_checks": total_checks,
        "total_passed_checks": total_passed,
        "overall_score": overall_score,
        "files": files_summary,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)