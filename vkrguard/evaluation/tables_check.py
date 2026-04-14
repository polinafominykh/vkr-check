import re
from vkrguard.schemes.results import CheckResult


def check_tables_references(text: str) -> CheckResult:
    matches = re.findall(r"таблица\s+\d+|табл\.\s*\d+", text.lower())
    found = len(matches) > 0

    return CheckResult(
        criterion_name="tables_references_presence",
        passed=found,
        comment="Упоминания таблиц найдены" if found else "Упоминания таблиц не найдены",
        details={
            "matches_count": len(matches),
            "sample_matches": matches[:10],
        },
    )