import pytest

from subclean.processors import Error, fixes, run


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("-dialog.", "- dialog."),
        ("- dialog.", "- dialog."),
        ("i-in", "i-in"),
        ("<i>-dialog.</i>", "<i>- dialog.</i>"),
        ("<i>-</i>dialog.", "<i>- </i>dialog."),
        ("-...dialog.", "- ...dialog."),
    ],
)
def test_clean_dashes(line: str, expected: str) -> None:
    assert fixes.clean_dashes(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("First sentence.Second sentence.", "First sentence. Second sentence."),
        ("First sentence...Second sentence.", "First sentence... Second sentence."),
    ],
)
def test_fix_spaces(line: str, expected: str) -> None:
    assert fixes.fix_spaces(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("First sentence.  Second   sentence.", "First sentence. Second sentence."),
        ("on my part, I mean,  utter idiocy. ", "on my part, I mean, utter idiocy."),
        ("", ""),
        (" ", ""),
        ("\u00a0", ""),
        ("test", "test"),
        (" test", "test"),
        (" test  ", "test"),
        ("test <i>", "test<i>"),
        ("test </i> ", "test</i>"),
        ("<i>  test", "<i>test"),
        (" <i>test", "<i>test"),
        ("  <i> test", "<i>test"),
        ("<i>test</i>", "<i>test</i>"),
        ("test test", "test test"),
        ("test  test", "test test"),
        ("test<i>  test", "test<i> test"),
        ("test  <i> test", "test <i>test"),
        (" test</i><i> </i> ", "test</i><i></i>"),
    ],
)
def test_trim_whitespace(line: str, expected: str) -> None:
    assert fixes.trim_whitespace(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "First sentence  . Second sentence ,  blabla.",
            "First sentence. Second sentence, blabla.",
        ),
        ("First sentence... Second sentence.", "First sentence... Second sentence."),
        ("Whoa ...", "Whoa..."),
        ("Whoa...", "Whoa..."),
        ("Yeah. ..maybe.", "Yeah...maybe."),
        ("Begin... ...end.", "Begin... ...end."),
        ("- ...dialog", "- ...dialog"),
        ("weighed as much as his .45.", "weighed as much as his .45."),
        ("black-handled .38", "black-handled .38"),
    ],
)
def test_fix_space_punctuation(line: str, expected: str) -> None:
    assert fixes.fix_space_punctuation(line) == expected


@pytest.mark.parametrize(
    ("fix", "line", "expected"),
    [
        (fixes.fix_hyphen, "'’", "'"),
        (fixes.fix_ampersand, "&amp;", "&"),
        (fixes.fix_quote, "&quot;", '"'),
        (fixes.fix_music, "# lalalala", "♪ lalalala"),
    ],
)
def test_replacements(fix: fixes.LineFix, line: str, expected: str) -> None:
    assert fix(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("<i></i>", ""),
        ("<i> </i>", " "),
        ("</i> <i>", " "),
        ("<i></i><i></i>", ""),
        ("<i></i> <i> </i> <i>sentence</i>", "   <i>sentence</i>"),
    ],
)
def test_fix_styles(line: str, expected: str) -> None:
    assert fixes.fix_styles(line) == expected


def test_error(load) -> None:
    cues = run(load("sub_error.srt"), [("Error", Error())])
    assert cues[0].lines == ("Madame... ...for you, I'll make it",)
