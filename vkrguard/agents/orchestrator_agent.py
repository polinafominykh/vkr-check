from pathlib import Path
from typing import List

from vkrguard.agents.formal_agent import FormalAgent
from vkrguard.agents.section_agent import SectionAgent
from vkrguard.agents.illustration_agent import IllustrationAgent
from vkrguard.agents.document_agent import DocumentAgent

from vkrguard.ingest.extract_pdf import extract_text_from_pdf
from vkrguard.ingest.extract_docx import extract_text_from_docx
from vkrguard.ingest.section_extractor import extract_sections
from vkrguard.schemes.results import EvaluationReport, CheckResult
from vkrguard.utils.recommendations import build_recommendations


class OrchestratorAgent:
    def __init__(self) -> None:
        self.formal_agent = FormalAgent()
        self.section_agent = SectionAgent()
        self.illustration_agent = IllustrationAgent()
        self.document_agent = DocumentAgent()

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

        formal_checks: List[CheckResult] = self.formal_agent.run(text, sections, file_path)
        section_checks: List[CheckResult] = self.section_agent.run(text, sections, file_path)
        illustration_checks: List[CheckResult] = self.illustration_agent.run(text, sections, file_path)
        document_checks: List[CheckResult] = self.document_agent.run(text, sections, file_path)

        all_document_checks = illustration_checks + document_checks
        all_checks = formal_checks + section_checks + all_document_checks

        passed_count = sum(1 for c in all_checks if c.passed)
        total_count = len(all_checks)
        score = round((passed_count / total_count) * 100, 2) if total_count else 0.0

        if score >= 85:
            overall_status = "good"
        elif score >= 60:
            overall_status = "warning"
        else:
            overall_status = "poor"

        failed_checks = [
            {
                "criterion_name": c.criterion_name,
                "comment": c.comment,
            }
            for c in all_checks
            if not c.passed
        ]

        recommendations = build_recommendations(all_checks)

        summary = {
            "passed_checks": passed_count,
            "total_checks": total_count,
            "score": score,
            "overall_status": overall_status,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
            "used_agents": [
                self.formal_agent.agent_name,
                self.section_agent.agent_name,
                self.illustration_agent.agent_name,
                self.document_agent.agent_name,
            ],
        }

        return EvaluationReport(
            file_path=file_path,
            found_sections=list(sections.keys()),
            formal_checks=formal_checks,
            section_checks=section_checks,
            document_checks=all_document_checks,
            summary=summary,
        )