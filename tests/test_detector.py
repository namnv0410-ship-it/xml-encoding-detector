from xml_encoding_detector import (
    detect_encoding,
)


def test_default_encoding():

    result = detect_encoding(
        b""
    )

    assert result.encoding == "utf-8"
    assert result.source == "default"
    assert result.confidence == 0.5


def test_utf8_bom():

    data = (
        b"\xef\xbb\xbf"
        b"<?xml version='1.0'?>"
    )

    result = detect_encoding(
        data
    )

    assert result.encoding == "utf-8"
    assert result.source == "bom"
    assert result.confidence == 1.0
