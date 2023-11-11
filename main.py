import argparse

from pymc_workflow_analyzer.analyzer import static_analyzer
from pymc_workflow_analyzer.report import generate_static_report, save_report

def main():
    """
    Analyze a PyMC Workflow.

    :return: None.
    """
    parser = argparse.ArgumentParser(description="Analyze a PyMC Workflow")
    parser.add_argument(
        "input", 
        nargs="?",  # This makes the argument optional
        help="Path to the Python script or URL to analyze"
    )
    parser.add_argument(
        "--file", 
        action="store_true", 
        help="Indicate that the input is a file path (default)"
    )
    parser.add_argument(
        "--url", 
        action="store_true", 
        help="Indicate that the input is a URL"
    )
    parser.add_argument(
        "--code", 
        action="store_true", 
        help="Indicate that the input is a raw string"
    )
    parser.add_argument(
        "--output", 
        help="Path to the file to save the report to"
    )

    args = parser.parse_args()

    # Determine the type of input based on the flags provided
    if args.url:
        input_type = "url"
    elif args.code:
        input_type = "code"
    else:  # Default to file if no specific flag is provided
        input_type = "file"

    # If no input is provided, prompt the user to provide one
    if args.input is None:
        parser.error("No input provided. Please provide a file path, URL, or a raw string.")

    analysis_data = static_analyzer(args.input, source_type=input_type)
    report_content = generate_static_report(analysis_data)

    print(report_content)
    if args.output:
        save_report(report_content, args.output)
    else:
        save_report(report_content)  # you can also pass a specific filepath


if __name__ == "__main__":
    main()
