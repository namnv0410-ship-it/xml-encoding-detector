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

    return DetectionResult(
        encoding="utf-8",
        confidence=0.5,
        source="default",
    )
