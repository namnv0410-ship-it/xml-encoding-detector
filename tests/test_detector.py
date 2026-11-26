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


def test_xml_declaration_utf8_alias():

    data = b'<?xml version="1.0" encoding="UTF8"?>'

    result = detect_encoding(data)

    assert result.encoding == "utf-8"

    assert result.source == "xml-declaration"


def test_shift_jis_alias():

    data = b'<?xml version="1.0" encoding="Shift-JIS"?>'

    result = detect_encoding(data)

    assert result.encoding == "shift_jis"

    assert result.source == "xml-declaration"


def test_normalize_utf16_alias():

    from xml_encoding_detector.detector import (
        normalize_encoding,
    )

    assert normalize_encoding("UTF16LE") == "utf-16-le"


def test_normalize_utf32_alias():

    from xml_encoding_detector.detector import (
        normalize_encoding,
    )

    assert normalize_encoding("UTF32BE") == "utf-32-be"


def test_normalize_unknown_encoding():

    from xml_encoding_detector.detector import (
        normalize_encoding,
    )

    assert normalize_encoding("GB18030") == "gb18030"


def test_xml_without_encoding():

    data = b'<?xml version="1.0"?>'

    result = detect_encoding(data)

    assert result.encoding == "utf-8"

    assert result.source == "default"


def test_normalize_windows_1258():

    from xml_encoding_detector.detector import (
        normalize_encoding,
    )

    assert normalize_encoding("windows-1258") == "cp1258"


def test_normalize_big5():

    from xml_encoding_detector.detector import (
        normalize_encoding,
    )

    assert normalize_encoding("BIG5") == "big5"


def test_well_formed_xml():

    from xml_encoding_detector import (
        is_xml_well_formed,
    )

    data = b"<root></root>"

    assert is_xml_well_formed(data) is True


def test_invalid_xml():

    from xml_encoding_detector import (
        is_xml_well_formed,
    )

    data = b"<root>"

    assert is_xml_well_formed(data) is False
