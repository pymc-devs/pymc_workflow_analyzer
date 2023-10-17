import argparse
import sys
from pymc_workflow_analyzer.analyzer import static_analyze
from pymc_workflow_analyzer.report import static_report_generator, save_report

def main():
    parser = argparse.ArgumentParser(description="Analyze a PyMC Workflow")
    parser.add_argument("filepath", help="Path to the Python script to analyze")
    args = parser.parse_args()

    try:
        analysis_data = static_analyze(args.filepath)
    except FileNotFoundError:
        print(f"Error: The file {args.filepath} does not exist.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You do not have the permission to read the file {args.filepath}.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: The file {args.filepath} contains syntax errors.\n{str(e)}")
        sys.exit(1)

    report_content = static_report_generator(analysis_data)
    print(report_content)

    try:
        save_report(report_content)  # you can also pass a specific filepath
    except IOError as e:
        print(f"Error: An error occurred while writing the report to a file.\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
