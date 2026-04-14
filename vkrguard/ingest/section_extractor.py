import re


SECTION_PATTERNS = {
    "contents": r"\b(содержание|оглавление)\b",
    "annotation": r"\b(аннотация|summary of a graduation thesis)\b",
    "introduction": r"\bвведение\b",
    "conclusion": r"\bзаключение\b",
    "references": r"\b(список используемых источников|список литературы|библиографический список)\b",
}


def find_section_positions(text: str) -> dict:
    positions = {}
    lower_text = text.lower()

    for section_name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, lower_text, re.IGNORECASE)
        if match:
            positions[section_name] = match.start()

    return positions


def extract_sections(text: str) -> dict:
    positions = find_section_positions(text)

    if not positions:
        return {"full_text": text}

    sorted_sections = sorted(positions.items(), key=lambda x: x[1])
    sections = {}

    for i, (section_name, start_pos) in enumerate(sorted_sections):
        end_pos = len(text)
        if i + 1 < len(sorted_sections):
            end_pos = sorted_sections[i + 1][1]

        sections[section_name] = text[start_pos:end_pos].strip()

    return sections