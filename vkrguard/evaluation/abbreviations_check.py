from vkrguard.schemes.results import CheckResult


def check_abbreviations_section(text: str) -> CheckResult:
    lower_text = text.lower()

    keywords = [
        "список сокращений",
        "список сокращении",
        "список сокращений и условных обозначений",
        "список сокращении и условных обозначении",
    ]

    found_keyword = None
    for keyword in keywords:
        if keyword in lower_text:
            found_keyword = keyword
            break

    found = found_keyword is not None

    return CheckResult(
        criterion_name="abbreviations_section_presence",
        passed=found,
        comment="Раздел со списком сокращений найден" if found else "Раздел со списком сокращений не найден",
        details={"matched_keyword": found_keyword},
    )