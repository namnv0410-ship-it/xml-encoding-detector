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

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.json"

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

    content = report.read_text(encoding="utf-8")

    assert '"files_scanned"' in content


def test_cli_csv_output(
    monkeypatch,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.csv"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--csv",
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

    content = report.read_text(encoding="utf-8")

    assert "file,valid,encoding,error" in content

    assert "test.xml" in content

    assert "test.xml" in content


def test_cli_stats_output(
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
            "--stats",
        ],
    )

    from xml_encoding_detector.cli import (
        main,
    )

    result = main()

    assert result == 0

    output = capsys.readouterr().out

    assert "Files scanned" in output

    assert "Encodings" in output

    assert "utf-8" in output


def test_cli_html_output(
    monkeypatch,
    tmp_path,
):

    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
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

    content = report.read_text(encoding="utf-8")

    assert "XML Encoding Audit Report" in content

    assert "<table" in content

    assert "test.xml" in content


def test_html_report_contains_encoding_distribution(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    result = main()

    assert result == 0

    content = report.read_text(encoding="utf-8")

    assert "Encoding Distribution" in content


def test_html_report_contains_distribution_columns(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "Encoding" in content
    assert "Count" in content
    assert "Percentage" in content


def test_html_report_contains_encoding_data(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "utf-8" in content
    assert "100.0%" in content


def test_html_report_contains_encoding_row(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "<td>utf-8</td>" in content


def test_html_report_contains_summary_section(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "Summary" in content


def test_html_report_contains_files_scanned_summary(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "Files Scanned" in content


def test_html_report_does_not_use_list_for_distribution(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "<ul>" not in content


def test_html_report_contains_top_encoding(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "Top Encoding" in content


def test_top_encoding_is_computed(
    monkeypatch,
    tmp_path,
):
    utf8_file = tmp_path / "utf8.xml"
    utf16_file1 = tmp_path / "utf16_1.xml"
    utf16_file2 = tmp_path / "utf16_2.xml"

    utf8_file.write_text(
        "<root/>",
        encoding="utf-8",
    )

    utf16_file1.write_text(
        "<root/>",
        encoding="utf-16",
    )

    utf16_file2.write_text(
        "<root/>",
        encoding="utf-16",
    )

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(tmp_path),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(
        encoding="utf-8",
    )

    assert "Top Encoding" in content
    assert "utf-16" in content


def test_html_report_contains_summary_cards(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert 'class="summary-card"' in content


def test_html_report_contains_four_summary_cards(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert content.count('class="summary-card"') == 4


def test_html_report_contains_card_title(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "<h3>" in content


def test_html_report_contains_summary_grid(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert 'class="summary-grid"' in content


def test_html_report_contains_summary_grid(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert 'class="summary-grid"' in content


def test_html_report_contains_style_block(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "<style>" in content


def test_html_report_contains_summary_grid_style(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.html"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--html",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    content = report.read_text(encoding="utf-8")

    assert "display:flex" in content


def test_package_has_main_module():
    from xml_encoding_detector import __main__

    assert __main__ is not None


def test_main_module_exposes_main():
    from xml_encoding_detector.__main__ import main

    assert callable(main)


def test_json_report_output(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--json",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    assert report.exists()


def test_csv_report_output(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"

    xml_file.write_text("<root></root>")

    report = tmp_path / "report.csv"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--csv",
            "--output",
            str(report),
        ],
    )

    assert main() == 0

    assert report.exists()

    content = report.read_text(encoding="utf-8")

    assert "file" in content
    assert "encoding" in content
    assert "test.xml" in content


def test_output_file_not_scanned(
    monkeypatch,
    tmp_path,
):
    xml_file = tmp_path / "test.xml"
    xml_file.write_text("<root/>")

    report = tmp_path / "report.csv"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "xml-encoding-detector",
            str(xml_file),
            "--csv",
            "--output",
            str(report),
        ],
    )

    assert main() == 0
    assert report.exists()
    content = report.read_text(encoding="utf-8")

    assert "report.csv" not in content
