import argparse

from pymc_workflow_analyzer.analyzer import static_analyzer
from pymc_workflow_analyzer.report import generate_static_report, save_report

def main():
    """
    Analyze a PyMC Workflow.

    :return: None.
    """
    parser = argparse.ArgumentParser(description="Analyze a PyMC Workflow")
    parser.add_argument("filepath", help="Path to the Python script to analyze")
    parser.add_argument("--output", help="Path to the file to save the report to")
    args = parser.parse_args()

    analysis_data = static_analyzer(args.filepath)
    report_content = generate_static_report(analysis_data)

    print(report_content)
    if args.output:
        save_report(report_content, args.output)
    else:
        save_report(report_content)  # you can also pass a specific filepath


if __name__ == "__main__":
    main()
