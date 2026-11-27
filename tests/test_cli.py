import sys

from xml_encoding_detector.cli import (
    main,
)


def test_cli_import():

    assert callable(main)


def test_cli_main_exists():

    result = main

    assert result is not None


def test_cli_name():

    assert main.__name__ == "main"


def test_cli_doc():

    assert main is not None


def test_cli_help(
    monkeypatch,
    capsys,
):

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            "--help",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "Usage:" in output


def test_cli_missing_file(
    monkeypatch,
    capsys,
):

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            "missing.xml",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "File not found" in output


def test_cli_valid_xml(
    monkeypatch,
    capsys,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "valid=True" in output

    assert "utf-8" in output


def test_cli_json_output(
    monkeypatch,
    capsys,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--json",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert '"valid"' in output

    assert '"encoding"' in output


def test_cli_summary(
    monkeypatch,
    capsys,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--summary",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "Files scanned" in output

    assert "Valid XML" in output


def test_cli_summary_json(
    monkeypatch,
    capsys,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--summary",
            "--json",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert '"files_scanned"' in output

    assert '"valid"' in output

    assert '"encodings"' in output


def test_cli_summary_recursive(
    monkeypatch,
    capsys,
    tmp_path,
):

    root = tmp_path / "samples"

    nested = root / "nested"

    nested.mkdir(parents=True)

    (root / "a.xml").write_text("<a></a>")

    (nested / "b.xml").write_text("<b></b>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(root),
            "--recursive",
            "--summary",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "Files scanned" in output

    assert "2" in output


def test_cli_wildcard(
    monkeypatch,
    capsys,
    tmp_path,
):

    (tmp_path / "a.xml").write_text("<a></a>")

    (tmp_path / "b.xml").write_text("<b></b>")

    pattern = str(tmp_path / "*.xml")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            pattern,
            "--summary",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert "Files scanned" in output

    assert "2" in output


def test_cli_wildcard_json(
    monkeypatch,
    capsys,
    tmp_path,
):

    (tmp_path / "a.xml").write_text("<a></a>")

    pattern = str(tmp_path / "*.xml")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            pattern,
            "--summary",
            "--json",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    main()

    output = capsys.readouterr().out

    assert '"files_scanned"' in output

    assert '"valid"' in output


def test_cli_invalid_xml_exit_code(
    monkeypatch,
    tmp_path,
):

    xml_file = tmp_path / "broken.xml"

    xml_file.write_text("<root>")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    result = main()

    assert result == 1
def test_cli_output_file(
    monkeypatch,
    tmp_path,
):

    xml_file = (
        tmp_path
        / "test.xml"
    )

    xml_file.write_text(
        "<root></root>"
    )

    report = (
        tmp_path
        / "report.json"
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--summary",
            "--json",
            "--output",
            str(report),
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    result = main()

    assert result == 0

    assert report.exists()

    content = (
        report.read_text(
            encoding="utf-8"
        )
    )

    assert (
        '"files_scanned"'
        in content
    )
def test_cli_csv_output(
    monkeypatch,
    tmp_path,
):

    xml_file = (
        tmp_path
        / "test.xml"
    )

    xml_file.write_text(
        "<root></root>"
    )

    report = (
        tmp_path
        / "report.csv"
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--csv",
            str(report),
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    result = main()

    assert result == 0

    assert report.exists()

    content = report.read_text(
        encoding="utf-8"
    )

    assert (
        "file,valid,encoding,error"
        in content
    )

    assert (
        "test.xml"
        in content
    )
def test_cli_csv_output(
    monkeypatch,
    tmp_path,
):

    xml_file = (
        tmp_path
        / "test.xml"
    )

    xml_file.write_text(
        "<root></root>"
    )

    report = (
        tmp_path
        / "report.csv"
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--csv",
            str(report),
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    result = main()

    assert result == 0

    assert report.exists()

    content = report.read_text(
        encoding="utf-8"
    )

    assert (
        "file,valid,encoding,error"
        in content
    )

    assert (
        "test.xml"
        in content
    )