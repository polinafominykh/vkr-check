import re


def check_required_sections(sections: dict) -> dict:
    required = ["introduction", "conclusion", "references"]
    missing = [section for section in required if section not in sections]

    return {
        "passed": len(missing) == 0,
        "missing_sections": missing,
        "found_sections": list(sections.keys()),
    }


def estimate_page_count(text: str) -> dict:
    chars_per_page = 3000
    estimated_pages = max(1, len(text) // chars_per_page + 1)

    return {
        "estimated_pages": estimated_pages,
        "passed_minimum": estimated_pages >= 40,
    }


def check_pdf_page_count(page_count: int, min_pages: int = 40) -> dict:
    return {
        "page_count": page_count,
        "passed_minimum": page_count >= min_pages,
        "minimum_required": min_pages,
    }


def check_references_in_text(text: str) -> dict:
    patterns = [
        r"\[\d+\]",
        r"\[\d+[-–]\d+\]",
        r"\(\s*[А-ЯA-Z][а-яa-z]+.*?\d{4}\s*\)",
    ]

    found_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        found_matches.extend(matches)

    return {
        "passed": len(found_matches) > 0,
        "matches_count": len(found_matches),
        "sample_matches": found_matches[:10],
    }