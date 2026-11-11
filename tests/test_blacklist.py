import pytest

from subclean.processors import Blacklist, run


@pytest.mark.parametrize(
    "line",
    [
        "Advertise your product or brand here",
        "contact www.OpenSubtitles.org today",
        '<font color="#ffff00">Provided by username</font>',
        "[http://example.com]",
        "http://foo.network",
        "Visit https://another-example.com",
        "find more under subs.link",
        "twitter.com/username",
    ],
)
def test_matches(line: str) -> None:
    assert Blacklist().matches(line)


def test_keeps_regular_dialog() -> None:
    assert not Blacklist().matches("I'll see you tomorrow.")


def test_extra_patterns() -> None:
    assert Blacklist.with_extra(r"\bfoo\b").matches("FOO bar")
    assert not Blacklist().matches("FOO bar")


def test_removes_ads(load) -> None:
    cues = load("sub_ads.srt")
    assert len(cues) == 3
    assert run(cues, [("Blacklist", Blacklist())]) == []
