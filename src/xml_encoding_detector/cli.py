import json
import sys
from pathlib import Path

from xml_encoding_detector import (
    validate_xml,
)


def main() -> int:

    if (
        len(sys.argv) < 2
        or sys.argv[1] in (
            "-h",
            "--help",
        )
    ):
        print(
            "Usage: xml-encoding-detector <file-or-directory> [more files...] [--json]"
        )
        return 1

    json_mode = (
        "--json" in sys.argv
    )

    inputs = [
        arg
        for arg in sys.argv[1:]
        if arg != "--json"
    ]

    paths = []

    for item in inputs:

        path = Path(
            item
        )

        if path.is_dir():

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

        if json_mode:

            results.append(
                {
                    "file": path.name,
                    "valid": result.valid,
                    "encoding": result.encoding,
                    "error": result.error,
                }
            )

        else:

            print(
                f"{path.name}: "
                f"valid={result.valid}, "
                f"encoding={result.encoding}"
            )

    if json_mode:

        print(
            json.dumps(
                results
            )
        )

    return 0
