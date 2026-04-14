from typing import List

from vkrguard.agents.base_agent import BaseAgent
from vkrguard.evaluation.chapter_check import check_main_chapters
from vkrguard.evaluation.reference_check import check_references_after_conclusion
from vkrguard.evaluation.order_check import check_basic_sections_order
from vkrguard.schemes.results import CheckResult


class DocumentAgent(BaseAgent):
    agent_name = "document_agent"

    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        return [
            check_main_chapters(text),
            check_references_after_conclusion(text),
            check_basic_sections_order(text),
        ]