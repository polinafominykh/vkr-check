from typing import List

from vkrguard.agents.base_agent import BaseAgent
from vkrguard.evaluation.figures_check import check_figures_references
from vkrguard.evaluation.tables_check import check_tables_references
from vkrguard.schemes.results import CheckResult


class IllustrationAgent(BaseAgent):
    agent_name = "illustration_agent"

    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        return [
            check_figures_references(text),
            check_tables_references(text),
        ]