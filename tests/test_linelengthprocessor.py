import pytest

from core.line import Line
from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import LineLengthProcessor


class TestLineLengthProcessor:
    @pytest.fixture()
    def subtitle(self) -> Subtitle:
        subtitle: Subtitle = SubtitleParser.load("linelength.srt")
        return subtitle

    @pytest.fixture()
    def processor(self, subtitle: Subtitle) -> LineLengthProcessor:
        return LineLengthProcessor(subtitle)

    def test_get_slices(self, processor: LineLengthProcessor):
        assert processor.get_slices([Line("hello"), Line("there")]) == [
            [
                Line("hello"),
                Line("there"),
            ]
        ]
        assert processor.get_slices([Line("- hello"), Line("there")]) == [
            [
                Line("- hello"),
                Line("there"),
            ]
        ]
        assert processor.get_slices([Line("hello"), Line("- there")]) == [
            [Line("hello")],
            [Line("- there")],
        ]
        assert processor.get_slices([Line("hello"), Line("- there"), Line("man")]) == [
            [Line("hello")],
            [Line("- there"), Line("man")],
        ]
        assert processor.get_slices([Line("- hi"), Line("- bye")]) == [
            [Line("- hi")],
            [Line("- bye")],
        ]
        assert processor.get_slices(
            [Line("- hi"), Line("bob"), Line("- bye"), Line("bob")]
        ) == [[Line("- hi"), Line("bob")], [Line("- bye"), Line("bob")]]
        assert processor.get_slices(
            [Line("hi"), Line("-bob"), Line("- bye"), Line("bob")]
        ) == [[Line("hi")], [Line("-bob")], [Line("- bye"), Line("bob")]]

    def test_merge_short_lines(self, processor: LineLengthProcessor):
        sections = processor.subtitle.sections
        section = processor.process_section(sections[0])
        assert len(section.lines) == 1
        assert section.lines[0] == "Go on now. What you got?"
        assert processor.process_section(sections[1]) == sections[1]
        section = processor.process_section(sections[2])
        assert len(section.lines) == 1
        assert section.lines[0] == "All right, let's pick up the pace."
        section = processor.process_section(sections[3])
        assert len(section.lines) == 1
        assert section.lines[0] == "- What if she's supposed to be with me?"
