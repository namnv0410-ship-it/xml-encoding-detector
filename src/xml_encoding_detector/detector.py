from dataclasses import dataclass


@dataclass(slots=True)
class DetectionResult:
    encoding: str
    confidence: float
    source: str


UTF8_BOM = b"\xef\xbb\xbf"

UTF16_LE_BOM = b"\xff\xfe"
UTF16_BE_BOM = b"\xfe\xff"

UTF32_LE_BOM = b"\xff\xfe\x00\x00"
UTF32_BE_BOM = b"\x00\x00\xfe\xff"


def detect_xml_declaration_encoding(
    data: bytes,
) -> str | None:

    head = data[:512]

    try:
        text = head.decode(
            "ascii",
            errors="ignore",
        )
    except Exception:
        return None

    marker = "encoding="

    index = text.lower().find(marker)

    if index == -1:
        return None

    value = text[index + len(marker) :].lstrip()

    if not value:
        return None

    quote = value[0]

    if quote not in (
        '"',
        "'",
    ):
        return None

    end = value.find(
        quote,
        1,
    )

    if end == -1:
        return None

    return value[1:end].lower()


def detect_encoding(
    data: bytes,
) -> DetectionResult:

    if data.startswith(UTF8_BOM):
        return DetectionResult(
            encoding="utf-8",
            confidence=1.0,
            source="bom",
        )

    if data.startswith(UTF32_LE_BOM):
        return DetectionResult(
            encoding="utf-32-le",
            confidence=1.0,
            source="bom",
        )

    if data.startswith(UTF32_BE_BOM):
        return DetectionResult(
            encoding="utf-32-be",
            confidence=1.0,
            source="bom",
        )

    if data.startswith(UTF16_LE_BOM):
        return DetectionResult(
            encoding="utf-16-le",
            confidence=1.0,
            source="bom",
        )

    if data.startswith(UTF16_BE_BOM):
        return DetectionResult(
            encoding="utf-16-be",
            confidence=1.0,
            source="bom",
        )

    declaration_encoding = detect_xml_declaration_encoding(data)

    if declaration_encoding:
        return DetectionResult(
            encoding=declaration_encoding,
            confidence=0.9,
            source="xml-declaration",
        )

    return DetectionResult(
        encoding="utf-8",
        confidence=0.5,
        source="default",
    )
