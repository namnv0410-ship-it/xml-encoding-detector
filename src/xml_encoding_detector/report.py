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
        file.write(
            "<html><body>"
        )

        file.write(
            "<h1>XML Encoding Audit Report</h1>"
        )
        file.write(
            "<h2>Summary</h2>"
        )
        file.write(
            '<div class="summary-card">'
        )
        file.write(
            f"<p>Files Scanned: {len(results)}</p>"
        )
        file.write(
            "</div>"
        )

        file.write(
            '<div class="summary-card">'
        )
        file.write(
            f"<p>Valid XML: {valid_count}</p>"
        )
        file.write(
            "</div>"
        )

        file.write(
            '<div class="summary-card">'
        )
        file.write(
            f"<p>Invalid XML: {invalid_count}</p>"
        )
        file.write(
            "</div>"
        )
        top_encoding = max(
            encodings.items(),
            key=lambda item: item[1],
        )[0]

        file.write(
            '<div class="summary-card">'
        )
        file.write(
            f"<p>Top Encoding: {top_encoding}</p>"
        )
        file.write(
            "</div>"
        )
        file.write(
            "<h2>Encoding Distribution</h2>"
        )
        file.write(
            "<table border='1'>"
        )

        file.write(
            "<tr>"
            "<th>Encoding</th>"
            "<th>Count</th>"
            "<th>Percentage</th>"
            "</tr>"
        )
        total = sum(
            encodings.values()
        )

        for (
            encoding,
            count,
        ) in sorted(
            encodings.items()
        ):
            percentage = (
                count
                / total
                * 100
            )

            file.write(
                "<tr>"
                f"<td>{encoding}</td>"
                f"<td>{count}</td>"
                f"<td>{percentage:.1f}%</td>"
                "</tr>"
            )        
        file.write("</table>")
        file.write(
            "<h2>File Results</h2>"
        )

        file.write(
            "<table border='1'>"
        )

        file.write(
            "<tr>"
            "<th>File</th>"
            "<th>Encoding</th>"
            "<th>Valid</th>"
            "</tr>"
        )
        for result in results:
            file.write(
                "<tr>"
                f"<td>{result['file']}</td>"
                f"<td>{result['encoding']}</td>"
                f"<td>{result['valid']}</td>"
                "</tr>"
            )
        file.write("</table>")
        file.write(
            "</body></html>"
        )
