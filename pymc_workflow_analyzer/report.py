import json

def format_list(key, value):
    """
    Format a list of dictionaries into a string.

    :param key: Key associated with the list.
    :param value: List of dictionaries to format.
    :return: Formatted string.
    """
    # Check if the list contains more than one dictionary
    if len(value) > 1 and all(isinstance(x, dict) for x in value):
        formatted = f'"{key}": [\n'
        for i, item in enumerate(value):
            # Add a tab character for inner dictionary
            formatted += '\t\t' + json.dumps(item)
            formatted += ',\n' if i != len(value) - 1 else '\n\t]'
    else:
        # If it's a single dictionary, keep it in one line
        formatted = f'"{key}": {json.dumps(value)}'
    return formatted


def format_json(data):
    """
    Format a dictionary into a JSON string with specific formatting rules.

    :param data: Dictionary to format.
    :return: Formatted JSON string.
    """
    formatted_json = "{\n"
    for key, value in data.items():
        # Format lists based on their content
        if isinstance(value, list) and value:
            formatted_json += '\t' + format_list(key, value)
        else:
            # Format other types in a single line
            formatted_json += f'\t"{key}": {json.dumps(value)}'
        
        # Add a comma and newline if this is not the last item
        if key != list(data.keys())[-1]:
            formatted_json += ',\n'
        
    formatted_json += "\n}"
    return formatted_json


def generate_static_report(analysis_data):
    """
    Generate a static report from analysis data.

    :param analysis_data: Dictionary containing analysis data.
    :return: Formatted JSON string.
    """
    """
    Generate a static report from analysis data.

    :param analysis_data: Dictionary containing analysis data.
    :return: Formatted JSON string.
    """
    return format_json(analysis_data)


def save_report(report_content, filepath="report.txt"):
    """
    Save report content to a file.

    :param report_content: Content to save.
    :param filepath: Path to file to save to.
    """
    try:
        with open(filepath, "w") as report_file:
            report_file.write(report_content)
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while saving the report.\n{str(e)}")
