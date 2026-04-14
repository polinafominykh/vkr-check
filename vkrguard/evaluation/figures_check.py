import re
from vkrguard.schemes.results import CheckResult


def check_figures_references(text: str) -> CheckResult:
    matches = re.findall(r"рисунок\s+\d+|рис\.\s*\d+", text.lower())
    found = len(matches) > 0

    return CheckResult(
        criterion_name="figures_references_presence",
        passed=found,
        comment="Упоминания рисунков найдены" if found else "Упоминания рисунков не найдены",
        details={
            "matches_count": len(matches),
            "sample_matches": matches[:10],
        },
    )