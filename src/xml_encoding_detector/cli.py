import csv
import glob
import json
import sys
from collections import Counter
from pathlib import Path

from xml_encoding_detector import validate_xml


def write_output(
    content: str,
    output_file: str | None,
) -> None:
    if output_file:
        Path(output_file).write_text(
            content,
            encoding="utf-8",
        )
    else:
        print(content)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in (
        "-h",
        "--help",
    ):
        print(
            "Usage: "
            "xml-encoding-detector "
            "<file-or-directory> "
            "[more files...] "
            "[--json] "
            "[--recursive] "
            "[--summary] "
            "[--output FILE]"
        )
        return 2

    json_mode = "--json" in sys.argv

    recursive_mode = "--recursive" in sys.argv

    summary_mode = "--summary" in sys.argv
    stats_mode = "--stats" in sys.argv

    output_file = None
    csv_file = None
    html_file = None

    if "--output" in sys.argv:
        index = sys.argv.index("--output")

        if index + 1 < len(sys.argv):
            output_file = sys.argv[index + 1]
    if "--csv" in sys.argv:
        index = sys.argv.index("--csv")

        if index + 1 < len(sys.argv):
            csv_file = sys.argv[index + 1]
    if "--html" in sys.argv:

        index = sys.argv.index(
            "--html"
        )

        if (
            index + 1
            < len(sys.argv)
        ):

            html_file = sys.argv[
                index + 1
            ] 

    skip_next = False

    inputs = []

    for arg in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue

        if arg == "--output":
            skip_next = True
            continue

        if arg == "--csv":
            skip_next = True
            continue
        if arg == "--html":

            skip_next = True
            continue

        if arg in (
            "--json",
            "--recursive",
            "--summary",
            "--stats",
            "--csv",
            "--html",
        ):
            continue

        inputs.append(arg)

    paths = []

    for item in inputs:
        if "*" in item or "?" in item or "[" in item:
            matches = glob.glob(
                item,
                recursive=True,
            )

            for match in matches:
                paths.append(Path(match))

            continue

        path = Path(item)

        if path.is_dir():
            if recursive_mode:
                paths.extend(sorted(path.rglob("*.xml")))

            else:
                paths.extend(sorted(path.glob("*.xml")))

        else:
            paths.append(path)

    results = []

    valid_count = 0
    invalid_count = 0

    encodings = Counter()

    for path in paths:
        if not path.exists():
            print(f"File not found: {path}")

            continue

        with open(
            path,
            "rb",
        ) as file:
            data = file.read()

        result = validate_xml(data)

        if result.valid:
            valid_count += 1

        else:
            invalid_count += 1

        if result.encoding:
            encodings[result.encoding] += 1

        results.append(
            {
                "file": path.name,
                "valid": result.valid,
                "encoding": result.encoding,
                "error": result.error,
            }
        )

        if not json_mode and not summary_mode:
            print(f"{path.name}: valid={result.valid}, encoding={result.encoding}")
    if csv_file:
        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "file",
                    "valid",
                    "encoding",
                    "error",
                ],
            )

            writer.writeheader()

            writer.writerows(results)
    if html_file:

        with open(
            html_file,
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
                f"<p>Files Scanned: {len(results)}</p>"
                f"{len(results)}</p>"
            )
            file.write(
                f"<p>Valid XML: "
                f"{valid_count}</p>"
            )
            top_encoding = max(
                encodings.items(),
                key=lambda item: item[1],
            )[0]
            file.write(
                f"<p>Top Encoding: {top_encoding}</p>"
            )
            file.write(
                f"<p>Invalid XML: "
                f"{invalid_count}</p>"
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
            file.write("</table>")
            total = sum(
                encodings.values()
            )

            if total:
              
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

            file.write(
                "</table>"
            )

            file.write(
                "</body></html>"
            )
    if stats_mode:
        print(f"Files scanned : {len(results)}")

        print()

        print("Encodings")

        print("---------")

        total = sum(encodings.values())

        for (
            encoding,
            count,
        ) in sorted(encodings.items()):
            percentage = count / total * 100

            print(f"{encoding:<15} {count:<5} ({percentage:.1f}%)")
    if summary_mode:
        summary = {
            "files_scanned": len(results),
            "valid": valid_count,
            "invalid": invalid_count,
            "encodings": dict(encodings),
        }

        if json_mode:
            content = json.dumps(
                summary,
                indent=2,
            )

            write_output(
                content,
                output_file,
            )

        else:
            print(f"Files scanned : {summary['files_scanned']}")

            print(f"Valid XML     : {summary['valid']}")

            print(f"Invalid XML   : {summary['invalid']}")

            print()

            print("Encodings")

            print("---------")

            for (
                encoding,
                count,
            ) in encodings.items():
                print(f"{encoding:<15} {count}")

    elif json_mode:
        content = json.dumps(
            results,
            indent=2,
        )

        write_output(
            content,
            output_file,
        )

    if invalid_count > 0:
        return 1

    return 0
