from pathlib import Path

from vkrguard.agents.orchestrator_agent import OrchestratorAgent
from vkrguard.utils.report_writer import save_report_to_json
from vkrguard.utils.batch_report_writer import save_batch_summary
from vkrguard.utils.csv_report_writer import save_batch_summary_csv


def main():
    input_folder = Path("data")
    output_folder = Path("reports/batch")

    if not input_folder.exists():
        print(f"Папка не найдена: {input_folder}")
        return

    supported_files = list(input_folder.glob("*.pdf")) + list(input_folder.glob("*.docx"))

    if not supported_files:
        print(f"В папке {input_folder} не найдено PDF или DOCX файлов")
        return

    orchestrator = OrchestratorAgent()
    reports = []

    print(f"Найдено файлов: {len(supported_files)}")

    for file_path in supported_files:
        print(f"\n=== Обработка: {file_path.name} ===")
        try:
            report = orchestrator.evaluate(str(file_path))
            reports.append(report)

            report_output_path = output_folder / f"{file_path.stem}.json"
            save_report_to_json(report, str(report_output_path))

            print(f"Статус: {report.summary}")
            print(f"Отчет сохранен: {report_output_path}")

        except Exception as e:
            print(f"Ошибка при обработке {file_path.name}: {e}")

    summary_json_path = output_folder / "summary.json"
    summary_csv_path = output_folder / "summary.csv"

    save_batch_summary(reports, str(summary_json_path))
    save_batch_summary_csv(reports, str(summary_csv_path))

    print("\n=== Batch-обработка завершена ===")
    print(f"Всего успешных отчетов: {len(reports)}")
    print(f"Сводный JSON-отчет сохранен: {summary_json_path}")
    print(f"Сводный CSV-отчет сохранен: {summary_csv_path}")


if __name__ == "__main__":
    main()