import pytest

from subclean import text


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("- <i>It's working.</i>", "- It's working."),
        (r"{\an8}appears at top", "appears at top"),
        (
            '<i>Previously on <font color="#ffff00">"TV Show"</font>...</i>',
            'Previously on "TV Show"...',
        ),
    ],
)
def test_strip_tags(line: str, expected: str) -> None:
    assert text.strip_tags(line) == expected
    assert text.visible_len(line) == len(expected)


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("", ""),
        (" ", ""),
        ("\u00a0", ""),
        ("test", "test"),
        (" test", "test"),
        (" test  ", "test"),
        ("test <i>", "test<i>"),
        ("<i>  test", "<i>test"),
        (" <i>test", "<i>test"),
        ("<i>test</i>", "<i>test</i>"),
    ],
)
def test_strip(line: str, expected: str) -> None:
    assert text.strip(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("- <i>This is a dialog.</i>", True),
        ("-this is also a dialog", True),
        ("<i>-dialog</i>", True),
        ("not a dialog", False),
    ],
)
def test_is_dialog(line: str, expected: bool) -> None:
    assert text.is_dialog(line) is expected
