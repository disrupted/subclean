import pytest

from subclean.processors import SDH, run, sdh


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("[camera shutter]", True),
        ("-[camera shutter]", True),
        ("-  [camera shutter]", True),
        ("(distant shouting))", True),
        ("[ distant shouting ]", True),
        ("♪", True),
        ("- ♪ ♪", True),
        ("♪ (SOFT PIANO MUSIC PLAYS)) ♪", True),
        ("(distant shouting,", False),
        ("weapons clashing))", False),
        ("-[journalists] Christine!", False),
        ("- TAMIKA: Yeah.", False),
    ],
)
def test_is_hi(line: str, expected: bool) -> None:
    assert sdh.is_hi(line) is expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("that's for you. [sighs]", True),
        ("‐TEACHER: blabla...", True),
        ("[Laura] sentence", True),
        ("<i>[Laura]</i> <i>sentence</i>", True),
        ("- CHRISTOPHER:<i> Hello?</i>", True),
        ("9:17 a.m., to be specific,", False),
        ("between 4:00 and 6:00.", False),
        ("I got some time between 4:00 and 6:00.", False),
    ],
)
def test_contains_hi(line: str, expected: bool) -> None:
    assert sdh.contains_hi(line) is expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("that's for you. [sighs]", "that's for you. "),
        ("‐TEACHER: blabla...", "‐blabla..."),
        ("[Laura] sentence", "sentence"),
        ("<i>[Laura]</i> <i>sentence</i>", "<i></i><i>sentence</i>"),
        ("- CHRISTOPHER:<i> Hello?</i>", "- <i>Hello?</i>"),
        ("9:17 a.m., to be specific,", "9:17 a.m., to be specific,"),
    ],
)
def test_clean_hi(line: str, expected: str) -> None:
    assert sdh.clean_hi(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("that's for you. [sighs]", "that's for you. "),
        (
            "on my part, I mean, [laughs] utter idiocy.",
            "on my part, I mean,  utter idiocy.",
        ),
        (
            "telling a joke [laughs], I mean, [continues laughing] you should've seen him.",
            "telling a joke , I mean,  you should've seen him.",
        ),
    ],
)
def test_clean_parentheses(line: str, expected: str) -> None:
    assert sdh.clean_parentheses(line) == expected


@pytest.mark.parametrize("line", ["♪", "- ♪ ♪"])
def test_is_simple_hi(line: str) -> None:
    assert sdh.is_simple_hi(line)


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("(distant shouting))", True),
        ("[ distant shouting ]", True),
        ("-[camera shutter]", True),
        ("(distant shouting,", False),
        ("weapons clashing))", False),
        ("[laughing nervously]:", False),
    ],
)
def test_is_parentheses(line: str, expected: bool) -> None:
    assert sdh.is_parentheses(line) is expected


@pytest.mark.parametrize(
    "line",
    [
        "♪ ominous music ♪",
        "- ♪ mysterious music ♪",
        " ♪ dramatic music ♪",
        "♪ upbeat music plays ♪",
        "♪ light orchestral music ♪",
        "♪ upbeat folk music playing ♪",
        "♪ swelling orchestral music plays ♪",
        "♪ upbeat song playing over speakers ♪",
        "♪ upbeat song playing over headphones ♪",
        "♪ soft, dramatic music ♪",
        "♪ music intensifies ♪",
        "♪ music swells ♪",
        "♪ dark music swells ♪",
        "♪ dramatic musical sting ♪",
        "♪ uneasy musical crescendo ♪",
        "♪ up‐tempo percussive music playing ♪",
        "<i>quiet, eerie music </i>",
        "<i>droning music fades in </i>",
        "<i>women vocalizing eerily </i>",
        "suspenseful, percussive music",
    ],
)
def test_is_music(line: str) -> None:
    assert sdh.is_music(line)


def test_is_not_music() -> None:
    assert not sdh.is_music("this is not a music subtitle")


def test_sdh(load) -> None:
    cues = load("sub_sdh.srt")
    assert len(cues) == 4
    result = run(cues, [("SDH", SDH())])
    assert len(result) == 2
    assert result[1].lines == ("I got some time", "between 4:00 and 6:00.")
