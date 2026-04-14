import re
from vkrguard.schemes.results import CheckResult


def check_main_chapters(text: str) -> CheckResult:
    chapter_matches = re.findall(r"\n\s*[1-9]\s+[А-ЯA-ZЁ]", text)
    found = len(chapter_matches) > 0

    return CheckResult(
        criterion_name="main_chapters_presence",
        passed=found,
        comment="Основные главы найдены" if found else "Основные главы не найдены",
        details={
            "matches_count": len(chapter_matches),
            "sample_matches": chapter_matches[:10],
        },
    )