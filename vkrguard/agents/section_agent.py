from typing import List

from vkrguard.agents.base_agent import BaseAgent
from vkrguard.evaluation.annotation_check import check_annotation
from vkrguard.evaluation.toc_check import check_table_of_contents
from vkrguard.evaluation.reference_check import check_references_section_size
from vkrguard.evaluation.abbreviations_check import check_abbreviations_section
from vkrguard.schemes.results import CheckResult


class SectionAgent(BaseAgent):
    agent_name = "section_agent"

    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        return [
            check_annotation(sections),
            check_table_of_contents(sections),
            check_references_section_size(sections),
            check_abbreviations_section(text),
        ]