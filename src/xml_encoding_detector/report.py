"""HTML reporting."""


def write_html_report(
    report_file,
    results,
    encodings,
    valid_count,
    invalid_count,
) -> None:
    with open(
        report_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write("<html><head>")
        file.write(
            "<style>"
            "body{font-family:Arial,sans-serif;padding:20px;}"
            ".summary-grid{display:flex;gap:16px;flex-wrap:wrap;}"
            ".summary-card{"
            "border:1px solid #ccc;"
            "padding:16px;"
            "min-width:180px;"
            "text-align:center;"
            "border-radius:8px;"
            "background:#f8f9fa;"
            "}"
            ".summary-card h3{margin:0;font-size:16px;}"
            ".summary-card p{"
            "font-size:36px;"
            "font-weight:bold;"
            "margin:12px 0 0 0;"
            "color:#0b5ed7;"
            "}"
            "table{border-collapse:collapse;}"
            "th,td{padding:8px;}"
            "</style>"
        )

        file.write("<h1>XML Encoding Audit Report</h1>")
        file.write("<h2>Summary</h2>")
        file.write('<div class="summary-grid">')
        file.write('<div class="summary-card">')
        file.write("<h3>Files Scanned</h3>")

        file.write(f"<p>{len(results)}</p>")
        file.write("</div>")

        file.write('<div class="summary-card">')
        file.write("<h3>Valid XML</h3>")

        file.write(f"<p>{valid_count}</p>")
        file.write("</div>")

        file.write('<div class="summary-card">')
        file.write("<h3>Invalid XML</h3>")

        file.write(f"<p>{invalid_count}</p>")
        file.write("</div>")
        top_encoding = max(
            encodings.items(),
            key=lambda item: item[1],
        )[0]

        file.write('<div class="summary-card">')
        file.write("<h3>Top Encoding</h3>")

        file.write(f"<p>{top_encoding}</p>")
        file.write("</div>")
        file.write("</div>")
        file.write("<h2>Encoding Distribution</h2>")
        file.write("<table border='1'>")

        file.write("<tr><th>Encoding</th><th>Count</th><th>Percentage</th></tr>")
        total = sum(encodings.values())

        for (
            encoding,
            count,
        ) in sorted(encodings.items()):
            percentage = count / total * 100

            file.write(
                "<tr>"
                f"<td>{encoding}</td>"
                f"<td>{count}</td>"
                f"<td>{percentage:.1f}%</td>"
                "</tr>"
            )
        file.write("</table>")
        file.write("<h2>File Results</h2>")

        file.write("<table border='1'>")

        file.write("<tr><th>File</th><th>Encoding</th><th>Valid</th></tr>")
        for result in results:
            file.write(
                "<tr>"
                f"<td>{result['file']}</td>"
                f"<td>{result['encoding']}</td>"
                f"<td>{result['valid']}</td>"
                "</tr>"
            )
        file.write("</table>")
        file.write("</body></html>")
