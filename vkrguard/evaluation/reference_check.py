import re
from vkrguard.schemes.results import CheckResult


def check_references_section_size(sections: dict) -> CheckResult:
    references_text = sections.get("references", "")
    lines = [line.strip() for line in references_text.splitlines() if line.strip()]

    source_lines = [
        line for line in lines
        if re.match(r"^\d+\.", line) or re.match(r"^\[\d+\]", line)
    ]

    count = len(source_lines)

    return CheckResult(
        criterion_name="references_section_size",
        passed=count >= 10,
        comment="Список источников выглядит содержательным" if count >= 10 else "Список источников слишком короткий",
        details={
            "sources_count": count,
            "sample_lines": source_lines[:10],
        },
    )


def check_references_after_conclusion(text: str) -> CheckResult:
    lower_text = text.lower()

    conclusion_pos = lower_text.find("заключение")
    references_pos = lower_text.find("список используемых источников")

    if references_pos == -1:
        references_pos = lower_text.find("список литературы")

    passed = conclusion_pos != -1 and references_pos != -1 and references_pos > conclusion_pos

    return CheckResult(
        criterion_name="references_after_conclusion",
        passed=passed,
        comment="Список источников расположен после заключения" if passed else "Порядок разделов нарушен",
        details={
            "conclusion_pos": conclusion_pos,
            "references_pos": references_pos,
        },
    )