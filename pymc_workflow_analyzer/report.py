def static_report_generator(data):
    report = f"""
Number of Import Statements: {len(data['imports'])}
Imports: {', '.join(data['imports'])}
Distributions: {', '.join(data['distributions'])}
Samplers: {data['samplers']}
    """
    return report.strip()  # strip() to remove leading/trailing white spaces

def save_report(report_content, filepath="report.txt"):
    with open(filepath, "w") as report_file:
        report_file.write(report_content)
