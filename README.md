XML Encoding Detector

A Python command-line tool for detecting XML encodings, validating XML files, and generating HTML, CSV, and JSON reports.



Features

Detect XML encodings

Validate XML documents

Scan directories recursively

Generate JSON reports

Generate CSV reports

Generate HTML dashboards

Summary statistics

Top encoding analysis

Installation

Development

git clone <repository-url>

cd xml-encoding-detector



pip install -e .

Wheel

pip install dist/xml\_encoding\_detector-0.4.0-py3-none-any.whl

Usage

Scan a file

xml-encoding-detector file.xml

Scan a directory

xml-encoding-detector sample

Recursive scan

xml-encoding-detector sample --recursive

JSON report

xml-encoding-detector sample --json --output report.json

CSV report

xml-encoding-detector sample --csv --output report.csv

HTML report

xml-encoding-detector sample --html --output report.html

Run as module

python -m xml\_encoding\_detector sample

Quality

62 automated tests

98% code coverage

GitHub Actions CI

Ruff formatting

Development

Run tests:



pytest

Run formatting:



ruff format .

Build package:



python -m build

License

MIT

Statistics

xml-encoding-detector sample --stats

Example output:



Encoding Statistics

===================



Files scanned : 42

Valid XML     : 40

Invalid XML   : 2



Top Encoding  : utf-8



utf-8         30 (71.4%)

utf-16        8 (19.0%)

cp1258        4 (9.5%)

Statistics

xml-encoding-detector sample --stats

Statistics JSON

xml-encoding-detector sample \\

&#x20; --stats \\

&#x20; --json \\

&#x20; --output stats.json

Markdown Report

xml-encoding-detector sample \\

&#x20; --markdown \\

&#x20; --output report.md

Features

