from vkrguard.schemes.results import CheckResult


def check_basic_sections_order(text: str) -> CheckResult:
    lower_text = text.lower()

    contents_pos = lower_text.find("содержание")
    introduction_pos = lower_text.find("введение")
    conclusion_pos = lower_text.find("заключение")
    references_pos = lower_text.find("список используемых источников")

    if references_pos == -1:
        references_pos = lower_text.find("список литературы")

    positions = {
        "contents": contents_pos,
        "introduction": introduction_pos,
        "conclusion": conclusion_pos,
        "references": references_pos,
    }

    valid_positions = [p for p in positions.values() if p != -1]
    passed = (
        contents_pos != -1
        and introduction_pos != -1
        and conclusion_pos != -1
        and references_pos != -1
        and contents_pos < introduction_pos < conclusion_pos < references_pos
    )

    return CheckResult(
        criterion_name="basic_sections_order",
        passed=passed,
        comment="Базовый порядок разделов корректный" if passed else "Базовый порядок разделов некорректный",
        details=positions,
    )