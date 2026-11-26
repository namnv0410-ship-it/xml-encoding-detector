from xml_encoding_detector.cli import (
    main,
)


def test_cli_import():

    assert callable(
        main
    )

def test_cli_main_exists():

    result = main

    assert result is not None
def test_cli_name():

    assert (
        main.__name__
        == "main"
    )
def test_cli_doc():

    assert (
        main is not None
    )
