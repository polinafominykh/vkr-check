from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class CheckResult:
    criterion_name: str
    passed: bool
    comment: str
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationReport:
    file_path: str
    found_sections: List[str]
    formal_checks: List[CheckResult]
    section_checks: List[CheckResult]
    document_checks: List[CheckResult]
    summary: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "found_sections": self.found_sections,
            "formal_checks": [c.to_dict() for c in self.formal_checks],
            "section_checks": [c.to_dict() for c in self.section_checks],
            "document_checks": [c.to_dict() for c in self.document_checks],
            "summary": self.summary,
        }