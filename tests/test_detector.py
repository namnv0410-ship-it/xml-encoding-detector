from xml_encoding_detector import (
    detect_encoding,
)


def test_default_encoding():

    result = detect_encoding(b"")

    assert result.encoding == "utf-8"
    assert result.source == "default"
    assert result.confidence == 0.5


def test_utf8_bom():

    data = b"\xef\xbb\xbf<?xml version='1.0'?>"

    result = detect_encoding(data)

    assert result.encoding == "utf-8"
    assert result.source == "bom"
    assert result.confidence == 1.0


def test_utf16_le_bom():

    data = b"\xff\xfe<\x00?\x00"

    result = detect_encoding(data)

    assert result.encoding == "utf-16-le"

    assert result.source == "bom"

    assert result.confidence == 1.0


def test_utf16_be_bom():

    data = b"\xfe\xff\x00<\x00?"

    result = detect_encoding(data)

    assert result.encoding == "utf-16-be"

    assert result.source == "bom"

    assert result.confidence == 1.0


def test_utf32_le_bom():

    data = b"\xff\xfe\x00\x00<\x00\x00\x00"

    result = detect_encoding(data)

    assert result.encoding == "utf-32-le"

    assert result.source == "bom"


def test_utf32_be_bom():

    data = b"\x00\x00\xfe\xff\x00\x00\x00<"

    result = detect_encoding(data)

    assert result.encoding == "utf-32-be"

    assert result.source == "bom"


def test_xml_declaration_utf8():

    data = b'<?xml version="1.0" encoding="UTF-8"?>'

    result = detect_encoding(data)

    assert result.encoding == "utf-8"

    assert result.source == "xml-declaration"


def test_xml_declaration_shift_jis():

    data = b'<?xml version="1.0" encoding="Shift_JIS"?>'

    result = detect_encoding(data)

    assert result.encoding == "shift_jis"

    assert result.source == "xml-declaration"
