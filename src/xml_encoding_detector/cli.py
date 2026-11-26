import json
import sys
from collections import Counter
from pathlib import Path

from xml_encoding_detector import (
    validate_xml,
)


def main() -> int:

    if (
        len(sys.argv) < 2
        or sys.argv[1]
        in (
            "-h",
            "--help",
        )
    ):
        print(
            "Usage: xml-encoding-detector "
            "<file-or-directory> "
            "[more files...] "
            "[--json] "
            "[--recursive] "
            "[--summary]"
        )
        return 1

    json_mode = (
        "--json"
        in sys.argv
    )

    recursive_mode = (
        "--recursive"
        in sys.argv
    )

    summary_mode = (
        "--summary"
        in sys.argv
    )

    inputs = [
        arg
        for arg in sys.argv[1:]
        if arg
        not in (
            "--json",
            "--recursive",
            "--summary",
        )
    ]

    paths = []

    for item in inputs:

        path = Path(
            item
        )

        if path.is_dir():

            if recursive_mode:

                paths.extend(
                    sorted(
                        path.rglob(
                            "*.xml"
                        )
                    )
                )

            else:

                paths.extend(
                    sorted(
                        path.glob(
                            "*.xml"
                        )
                    )
                )

        else:

            paths.append(
                path
            )

    results = []

    valid_count = 0
    invalid_count = 0

    encodings = Counter()

    for path in paths:

        if not path.exists():

            print(
                f"File not found: {path}"
            )

            continue

        with open(
            path,
            "rb",
        ) as file:

            data = file.read()

        result = validate_xml(
            data
        )

        if result.valid:

            valid_count += 1

        else:

            invalid_count += 1

        if result.encoding:

            encodings[
                result.encoding
            ] += 1

        entry = {
            "file": path.name,
            "valid": result.valid,
            "encoding": result.encoding,
            "error": result.error,
        }

        results.append(
            entry
        )

        if (
            not json_mode
            and not summary_mode
        ):

            print(
                f"{path.name}: "
                f"valid={result.valid}, "
                f"encoding={result.encoding}"
            )

    if summary_mode:

        summary = {
            "files_scanned": len(
                results
            ),
            "valid": valid_count,
            "invalid": invalid_count,
            "encodings": dict(
                encodings
            ),
        }

        if json_mode:

            print(
                json.dumps(
                    summary,
                    indent=2,
                )
            )

        else:

            print(
                f"Files scanned : "
                f"{summary['files_scanned']}"
            )

            print(
                f"Valid XML     : "
                f"{summary['valid']}"
            )

            print(
                f"Invalid XML   : "
                f"{summary['invalid']}"
            )

            print()

            print(
                "Encodings"
            )

            print(
                "---------"
            )

            for (
                encoding,
                count,
            ) in encodings.items():

                print(
                    f"{encoding:<15} "
                    f"{count}"
                )

    elif json_mode:

        print(
            json.dumps(
                results,
                indent=2,
            )
        )

    return 0