from dataclasses import dataclass


@dataclass(slots=True)
class DetectionResult:
    encoding: str
    confidence: float
    source: str


UTF8_BOM = b"\xef\xbb\xbf"

UTF16_LE_BOM = b"\xff\xfe"

UTF16_BE_BOM = b"\xfe\xff"


def detect_encoding(
    data: bytes,
) -> DetectionResult:

    if data.startswith(UTF8_BOM):
        return DetectionResult(
            encoding="utf-8",
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
