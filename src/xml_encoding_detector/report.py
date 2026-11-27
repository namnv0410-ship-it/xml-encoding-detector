"""HTML reporting."""
def write_html_report(
    report_file,
    results,
    encodings,
) -> None:
    with open(
        report_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
           "<html><body>"
        )
        pass