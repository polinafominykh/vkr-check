from typing import List

from vkrguard.agents.base_agent import BaseAgent
from vkrguard.schemes.results import CheckResult


class IntroductionSemanticAgent(BaseAgent):
    agent_name = "introduction_semantic_agent"

    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        return [
            CheckResult(
                criterion_name="introduction_semantic_stub",
                passed=True,
                comment="LLM-блок",
                details={"status": "stub"},
            )
        ]