from vkrguard.agents.orchestrator_agent import OrchestratorAgent
from vkrguard.utils.report_writer import save_report_to_json


def main():
    file_path = "data/sample.pdf"
    output_path = "reports/report.json"

    orchestrator = OrchestratorAgent()
    report = orchestrator.evaluate(file_path)

    print("=== Найденные разделы ===")
    for section_name in report.found_sections:
        print(f"- {section_name}")

    print("\n=== Формальные проверки ===")
    for check in report.formal_checks:
        print(f"{check.criterion_name}: {check.passed} | {check.comment}")

    print("\n=== Проверки по разделам ===")
    for check in report.section_checks:
        print(f"{check.criterion_name}: {check.passed} | {check.comment}")

    print("\n=== Проверки всей работы ===")
    for check in report.document_checks:
        print(f"{check.criterion_name}: {check.passed} | {check.comment}")

    print("\n=== Итог ===")
    print(report.summary)

    save_report_to_json(report, output_path)
    print(f"\nОтчет сохранен в {output_path}")


if __name__ == "__main__":
    main()