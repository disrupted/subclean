from datetime import timedelta
from pathlib import Path

import pytest

from subclean import formats, io
from subclean.cue import Cue
from subclean.formats.srt import SrtFormat

srt = SrtFormat()


def test_parse(load) -> None:
    cues = load("sub.srt")
    assert len(cues) == 667
    assert len(cues[0].lines) == 1
    assert "NETFLIX" in cues[0].lines[0]
    assert cues[13].lines == ("- Are you nervous?", "- A little.")
    assert cues[13].start == timedelta(minutes=1, seconds=29, milliseconds=605)
    assert cues[13].end == timedelta(minutes=1, seconds=31, milliseconds=645)
    assert "Translated by" in cues[-1].text


def test_numeric_text_is_kept() -> None:
    cues = srt.parse(
        "1\n00:00:01,000 --> 00:00:02,000\n1984\n42\n\n2\n00:00:03,000 --> 00:00:04,000\nfoo\n"
    )
    assert [cue.lines for cue in cues] == [("1984", "42"), ("foo",)]


def test_text_before_first_cue_is_ignored() -> None:
    assert srt.parse("garbage\n1\n00:00:01,000 --> 00:00:02,000\nfoo\n")[0].lines == (
        "foo",
    )


def test_roundtrip() -> None:
    text = "1\n01:02:03,004 --> 01:02:05,000\nhello\nthere\n\n2\n00:00:06,000 --> 00:00:07,500\nbye\n\n"
    assert srt.dump(srt.parse(text)) == text


def test_dump() -> None:
    cue = Cue(timedelta(seconds=1), timedelta(seconds=2, milliseconds=5), ("a", "b"))
    assert srt.dump([cue]) == "1\n00:00:01,000 --> 00:00:02,005\na\nb\n\n"


def test_unsupported_format() -> None:
    with pytest.raises(formats.UnsupportedFormatError, match=r"\.ass"):
        formats.for_path(Path("movie.ass"))


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("über".encode(), "über"),
        (b"\xef\xbb\xbfbom", "bom"),
        ("über".encode("cp1252"), "über"),
        (b"\x81", "\x81"),
    ],
)
def test_decode(data: bytes, expected: str) -> None:
    assert io.decode(data) == expected
