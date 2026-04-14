from vkrguard.schemes.results import CheckResult


def check_annotation(sections: dict) -> CheckResult:
    has_annotation = "annotation" in sections

    return CheckResult(
        criterion_name="annotation_presence",
        passed=has_annotation,
        comment="Аннотация найдена" if has_annotation else "Аннотация не найдена",
        details={"found": has_annotation},
    )