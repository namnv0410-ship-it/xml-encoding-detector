import sys
from pathlib import Path

from xml_encoding_detector import (
    validate_xml,
)


def main() -> int:

    if len(sys.argv) < 2 or sys.argv[1] in (
        "-h",
        "--help",
    ):
        print("Usage: xml-encoding-detector <file>")
        return 1

    path = sys.argv[1]

    if not Path(path).exists():
        print(f"File not found: {path}")

        return 1

    with open(
        path,
        "rb",
    ) as file:
        data = file.read()

    result = validate_xml(data)

    print(f"XML valid : {result.valid}")

    print(f"Encoding  : {result.encoding}")

    print(f"Error     : {result.error}")

    return 0
