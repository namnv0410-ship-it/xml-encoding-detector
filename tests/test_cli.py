from xml_encoding_detector.cli import (
    main,
)


def test_cli_import():

    assert callable(main)
