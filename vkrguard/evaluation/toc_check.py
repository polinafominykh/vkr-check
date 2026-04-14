from vkrguard.schemes.results import CheckResult


def check_table_of_contents(sections: dict) -> CheckResult:
    has_contents = "contents" in sections

    return CheckResult(
        criterion_name="table_of_contents_presence",
        passed=has_contents,
        comment="Содержание найдено" if has_contents else "Содержание не найдено",
        details={"found": has_contents},
    )