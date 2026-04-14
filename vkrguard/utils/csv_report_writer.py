import csv
from pathlib import Path
from typing import List

from vkrguard.schemes.results import EvaluationReport


def save_batch_summary_csv(reports: List[EvaluationReport], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "file_path",
            "score",
            "overall_status",
            "passed_checks",
            "total_checks",
            "failed_checks_count",
        ])

        for report in reports:
            summary = report.summary or {}
            failed_checks = summary.get("failed_checks", [])

            writer.writerow([
                report.file_path,
                summary.get("score", 0.0),
                summary.get("overall_status", "unknown"),
                summary.get("passed_checks", 0),
                summary.get("total_checks", 0),
                len(failed_checks),
            ])