from typing import List

from vkrguard.agents.base_agent import BaseAgent
from vkrguard.evaluation.formal_checks import (
    check_required_sections,
    check_pdf_page_count,
    estimate_page_count,
    check_references_in_text,
)
from vkrguard.ingest.extract_pdf import get_pdf_page_count
from vkrguard.schemes.results import CheckResult


class FormalAgent(BaseAgent):
    agent_name = "formal_agent"

    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        checks: List[CheckResult] = []

        required_sections_result = check_required_sections(sections)
        checks.append(
            CheckResult(
                criterion_name="required_sections_presence",
                passed=required_sections_result["passed"],
                comment="Все обязательные разделы найдены"
                if required_sections_result["passed"]
                else "Не все обязательные разделы найдены",
                details=required_sections_result,
            )
        )

        references_result = check_references_in_text(text)
        checks.append(
            CheckResult(
                criterion_name="references_in_text_presence",
                passed=references_result["passed"],
                comment="Ссылки в тексте найдены"
                if references_result["passed"]
                else "Ссылки в тексте не найдены",
                details=references_result,
            )
        )

        if file_path.lower().endswith(".pdf"):
            page_count = get_pdf_page_count(file_path)
            page_result = check_pdf_page_count(page_count)
            checks.append(
                CheckResult(
                    criterion_name="page_count_check",
                    passed=page_result["passed_minimum"],
                    comment="Объем соответствует минимуму"
                    if page_result["passed_minimum"]
                    else "Объем меньше минимального",
                    details=page_result,
                )
            )
        else:
            page_result = estimate_page_count(text)
            checks.append(
                CheckResult(
                    criterion_name="page_count_estimate",
                    passed=page_result["passed_minimum"],
                    comment="Оценка объема соответствует минимуму"
                    if page_result["passed_minimum"]
                    else "Оценка объема меньше минимального",
                    details=page_result,
                )
            )

        return checks