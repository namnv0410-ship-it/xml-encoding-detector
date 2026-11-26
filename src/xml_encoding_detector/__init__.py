from .detector import (
    get_xml_encoding,
    DetectionResult,
    ValidationResult,
    detect_encoding,
    is_xml_well_formed,
    validate_xml,
)

__all__ = [
    "get_xml_encoding",
    "DetectionResult",
    "detect_encoding",
    "is_xml_well_formed",
]
