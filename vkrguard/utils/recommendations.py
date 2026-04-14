from typing import List

from vkrguard.schemes.results import CheckResult


RECOMMENDATION_MAP = {
    "required_sections_presence": "Добавить отсутствующие обязательные разделы: введение, заключение, список источников.",
    "references_in_text_presence": "Добавить ссылки на источники в основном тексте работы.",
    "page_count_check": "Проверить объем работы: количество страниц ниже минимального порога.",
    "page_count_estimate": "Проверить ориентировочный объем документа.",
    "annotation_presence": "Добавить аннотацию к ВКР.",
    "table_of_contents_presence": "Добавить содержание.",
    "references_section_size": "Расширить список используемых источников.",
    "abbreviations_section_presence": "Добавить список сокращений и условных обозначений.",
    "figures_references_presence": "Добавить или проверить упоминания рисунков в тексте.",
    "tables_references_presence": "Добавить или проверить упоминания таблиц в тексте.",
    "main_chapters_presence": "Проверить наличие и оформление основных глав.",
    "references_after_conclusion": "Переместить список источников после заключения.",
    "basic_sections_order": "Проверить порядок основных разделов документа.",
}


def build_recommendations(checks: List[CheckResult]) -> List[str]:
    recommendations = []

    for check in checks:
        if not check.passed:
            recommendation = RECOMMENDATION_MAP.get(
                check.criterion_name,
                f"Требуется доработка по критерию: {check.criterion_name}.",
            )
            recommendations.append(recommendation)

    # убираем дубли, сохраняя порядок
    unique_recommendations = []
    seen = set()

    for rec in recommendations:
        if rec not in seen:
            unique_recommendations.append(rec)
            seen.add(rec)

    return unique_recommendations