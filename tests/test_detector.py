from xml_encoding_detector import (
    detect_encoding,
)


def test_detect_encoding_returns_utf8():

    result = detect_encoding(b"")

    assert result == "utf-8"
