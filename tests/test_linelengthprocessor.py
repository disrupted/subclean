from pathlib import Path

import pytest

from subclean.core.line import Line
from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import LineLengthProcessor


class TestLineLengthProcessor:
    @pytest.fixture()
    def subtitle(self) -> Subtitle:
        subtitle: Subtitle = SubtitleParser.load(
            Path("tests/resources/sub_linelength.srt")
        )
        return subtitle

    @pytest.fixture()
    def processor(self, subtitle: Subtitle) -> LineLengthProcessor:
        return LineLengthProcessor(subtitle)

    def test_split_dialog_chunks(self, processor: LineLengthProcessor):
        assert processor.split_dialog_chunks([Line("hello"), Line("there")]) == [
            [
                Line("hello"),
                Line("there"),
            ]
        ]
        assert processor.split_dialog_chunks([Line("- hello"), Line("there")]) == [
            [
                Line("- hello"),
                Line("there"),
            ]
        ]
        assert processor.split_dialog_chunks([Line("hello"), Line("- there")]) == [
            [Line("hello")],
            [Line("- there")],
        ]
        assert processor.split_dialog_chunks(
            [Line("hello"), Line("- there"), Line("man")]
        ) == [
            [Line("hello")],
            [Line("- there"), Line("man")],
        ]
        assert processor.split_dialog_chunks([Line("- hi"), Line("- bye")]) == [
            [Line("- hi")],
            [Line("- bye")],
        ]
        assert processor.split_dialog_chunks(
            [Line("- hi"), Line("bob"), Line("- bye"), Line("bob")]
        ) == [[Line("- hi"), Line("bob")], [Line("- bye"), Line("bob")]]
        assert processor.split_dialog_chunks(
            [Line("hi"), Line("-bob"), Line("- bye"), Line("bob")]
        ) == [[Line("hi")], [Line("-bob")], [Line("- bye"), Line("bob")]]
        assert processor.split_dialog_chunks(
            [Line("-I'm gonna call the police,"), Line("this can't keep happening.")]
        ) == [[Line("-I'm gonna call the police,"), Line("this can't keep happening.")]]

    def test_merge_short_lines(self, processor: LineLengthProcessor):
        sections = processor.subtitle.sections
        section = processor.process_section(sections[0])
        assert len(section) == 1
        assert section.lines[0] == "Go on now. What you got?"
        assert processor.process_section(sections[1]) == sections[1]
        section = processor.process_section(sections[2])
        assert len(section) == 1
        assert section.lines[0] == "All right, let's pick up the pace."
        section = processor.process_section(sections[3])
        assert len(section) == 1
        assert section.lines[0] == "- What if she's supposed to be with me?"
        assert processor.process_section(sections[4]) == sections[4]
