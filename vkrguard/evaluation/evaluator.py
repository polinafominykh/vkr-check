from pathlib import Path

from vkrguard.ingest.extract_pdf import extract_text_from_pdf, get_pdf_page_count
from vkrguard.ingest.extract_docx import extract_text_from_docx
from vkrguard.ingest.section_extractor import extract_sections

from vkrguard.evaluation.formal_checks import (
    check_required_sections,
    check_pdf_page_count,
    estimate_page_count,
    check_references_in_text,
)
from vkrguard.evaluation.annotation_check import check_annotation
from vkrguard.evaluation.toc_check import check_table_of_contents
from vkrguard.evaluation.figures_check import check_figures_references
from vkrguard.evaluation.chapter_check import check_main_chapters
from vkrguard.evaluation.reference_check import (
    check_references_section_size,
    check_references_after_conclusion,
)
from vkrguard.evaluation.order_check import check_basic_sections_order
from vkrguard.evaluation.tables_check import check_tables_references
from vkrguard.evaluation.abbreviations_check import check_abbreviations_section

from vkrguard.schemes.results import CheckResult, EvaluationReport


class VKRGuardEvaluator:
    def extract_text(self, file_path: str) -> str:
        lower_path = file_path.lower()

        if lower_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        if lower_path.endswith(".docx"):
            return extract_text_from_docx(file_path)

        raise ValueError("Поддерживаются только PDF и DOCX файлы")

    def evaluate(self, file_path: str) -> EvaluationReport:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        text = self.extract_text(file_path)
        sections = extract_sections(text)

        formal_checks = []
        section_checks = []
        document_checks = []

        required_sections_result = check_required_sections(sections)
        formal_checks.append(
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
        formal_checks.append(
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
            formal_checks.append(
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
            formal_checks.append(
                CheckResult(
                    criterion_name="page_count_estimate",
                    passed=page_result["passed_minimum"],
                    comment="Оценка объема соответствует минимуму"
                    if page_result["passed_minimum"]
                    else "Оценка объема меньше минимального",
                    details=page_result,
                )
            )

        section_checks.append(check_annotation(sections))
        section_checks.append(check_table_of_contents(sections))
        section_checks.append(check_references_section_size(sections))
        section_checks.append(check_abbreviations_section(text))

        document_checks.append(check_figures_references(text))
        document_checks.append(check_tables_references(text))
        document_checks.append(check_main_chapters(text))
        document_checks.append(check_references_after_conclusion(text))
        document_checks.append(check_basic_sections_order(text))

        all_checks = formal_checks + section_checks + document_checks
        passed_count = sum(1 for c in all_checks if c.passed)
        total_count = len(all_checks)
        score = round((passed_count / total_count) * 100, 2) if total_count else 0.0

        if score >= 85:
            overall_status = "good"
        elif score >= 60:
            overall_status = "warning"
        else:
            overall_status = "poor"

        summary = {
            "passed_checks": passed_count,
            "total_checks": total_count,
            "score": score,
            "overall_status": overall_status,
        }

        return EvaluationReport(
            file_path=file_path,
            found_sections=list(sections.keys()),
            formal_checks=formal_checks,
            section_checks=section_checks,
            document_checks=document_checks,
            summary=summary,
        )