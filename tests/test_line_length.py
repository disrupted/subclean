import pytest

from subclean.processors import LineLength
from subclean.processors.line_length import split_dialog


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        (["hello", "there"], [["hello", "there"]]),
        (["- hello", "there"], [["- hello", "there"]]),
        (["hello", "- there"], [["hello"], ["- there"]]),
        (["hello", "- there", "man"], [["hello"], ["- there", "man"]]),
        (["- hi", "- bye"], [["- hi"], ["- bye"]]),
        (["- hi", "bob", "- bye", "bob"], [["- hi", "bob"], ["- bye", "bob"]]),
        (["hi", "-bob", "- bye", "bob"], [["hi"], ["-bob"], ["- bye", "bob"]]),
        (
            ["-I'm gonna call the police,", "this can't keep happening."],
            [["-I'm gonna call the police,", "this can't keep happening."]],
        ),
        ([], []),
    ],
)
def test_split_dialog(lines: list[str], expected: list[list[str]]) -> None:
    assert split_dialog(lines) == expected


def test_merge_short_lines(load) -> None:
    cues = load("sub_linelength.srt")
    assert [cue.lines for cue in LineLength()(cues)] == [
        ("Go on now. What you got?",),
        cues[1].lines,
        ("All right, let's pick up the pace.",),
        ("- What if she's supposed to be with me?",),
        cues[4].lines,
    ]


def test_max_length(load) -> None:
    cues = load("sub_linelength.srt")
    assert LineLength(max_length=10)(cues) == cues
