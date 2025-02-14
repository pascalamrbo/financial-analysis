import datetime

def generate_html_report(results_dict):
    """
    Generates an HTML report summarizing validation results.
    results_dict format:
      {
         "fileA.xlsx": {"errors": [...], "warnings": [...]},
         "fileB.xlsx": {"errors": [...], "warnings": [...]},
      }
    Returns an HTML string.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_errors = sum(len(v["errors"]) for v in results_dict.values())
    total_warnings = sum(len(v["warnings"]) for v in results_dict.values())

    html = [
        "<html>",
        "<head>",
        "<title>Validation Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; }",
        ".error { color: red; }",
        ".warning { color: orange; }",
        ".file-section { margin-bottom: 20px; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>Financial Validation Report</h1>",
        f"<p>Generated on: {now}</p>",
        f"<p><strong>Total Errors: {total_errors}, Total Warnings: {total_warnings}</strong></p>",
        "<hr/>"
    ]

    for fname, outcome in results_dict.items():
        errors = outcome.get("errors", [])
        warnings = outcome.get("warnings", [])
        html.append(f"<div class='file-section'><h2>{fname}</h2>")
        if errors:
            html.append("<h3 class='error'>Errors:</h3><ul>")
            for e in errors:
                html.append(f"<li>{e}</li>")
            html.append("</ul>")
        if warnings:
            html.append("<h3 class='warning'>Warnings:</h3><ul>")
            for w in warnings:
                html.append(f"<li>{w}</li>")
            html.append("</ul>")
        if not errors and not warnings:
            html.append("<p>No issues found.</p>")
        html.append("</div>")
    html.append("</body></html>")
    return "\n".join(html)
