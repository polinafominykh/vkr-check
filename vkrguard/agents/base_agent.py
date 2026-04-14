from abc import ABC, abstractmethod
from typing import List

from vkrguard.schemes.results import CheckResult


class BaseAgent(ABC):
    agent_name: str = "base_agent"

    @abstractmethod
    def run(self, text: str, sections: dict, file_path: str) -> List[CheckResult]:
        pass