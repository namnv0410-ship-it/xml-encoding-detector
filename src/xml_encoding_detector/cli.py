import csv
import glob
import json
import sys
from collections import Counter
from pathlib import Path

from xml_encoding_detector import validate_xml
from .report import (
    write_html_report,
)


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
    stats_mode = "--stats" in sys.argv

    recursive_mode = "--recursive" in sys.argv

    summary_mode = "--summary" in sys.argv
    stats_mode = "--stats" in sys.argv

    output_file = None
    if "--output" in sys.argv:
        index = sys.argv.index("--output")
        if index + 1 < len(sys.argv):
            output_file = sys.argv[index + 1]
    csv_mode = "--csv" in sys.argv

    html_mode = "--html" in sys.argv

    skip_next = False

    inputs = []

    for arg in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue

        if arg == "--output":
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
        
    if csv_mode and output_file:
        with open(
            output_file,
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
        
    if html_mode and output_file:
        print(f"Writing HTML report to: {output_file}")
        write_html_report(
            output_file,
            results,
            encodings,
            valid_count,
            invalid_count,
        )

    if stats_mode:
        print()
        print("Encoding Statistics")
        print("===================")
        print()

        print(
            f"Files scanned : {len(results)}"
        )

        valid_count = sum(
            1
            for result in results
            if result["valid"]
        )

        invalid_count = (
            len(results)
            - valid_count
        )

        print(
            f"Valid XML     : {valid_count}"
        )

        print(
            f"Invalid XML   : {invalid_count}"
        )

        print()

        top_encoding = (
            encodings.most_common(1)[0][0]
        )
        stats_data = {
            "files_scanned": len(results),
            "valid_xml": valid_count,
            "invalid_xml": invalid_count,
            "top_encoding": top_encoding,
            "encodings": dict(encodings),
        }

        print(
            f"Top Encoding  : {top_encoding}"
        )

        print()
        print("Encodings")
        print("---------")
        if (
            json_mode
            and output_file
        ):
            with open(
                output_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    stats_data,
                    file,
                    indent=2,
                )

        total = sum(
            encodings.values()
        )

        for (
            encoding,
            count,
        ) in encodings.most_common():
            percentage = (
                count / total * 100
        )

            print(
                f"{encoding:<15}"
                f"{count:<5}"
                f"({percentage:.1f}%)"
            )
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

    elif json_mode and not stats_mode:
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


if __name__ == "__main__":
    raise SystemExit(main())
