from pathlib import Path
from unittest.mock import MagicMock

import pytest

from subclean.core.line import Line
from subclean.core.parser import SubtitleParser
from subclean.processors.processor import ErrorProcessor


class TestErrorProcessor:
    @pytest.fixture()
    def processor(self) -> ErrorProcessor:
        subtitle = MagicMock()
        return ErrorProcessor(subtitle)

    @pytest.fixture()
    def sub_processor(self) -> ErrorProcessor:
        subtitle = SubtitleParser.load(Path("tests/resources/sub_error.srt"))
        return ErrorProcessor(subtitle)

    def test_fix_spaces(self, processor: ErrorProcessor):
        assert (
            processor.fix_spaces(Line("First sentence.Second sentence."))
            == "First sentence. Second sentence."
        )
        assert (
            processor.fix_spaces(Line("First sentence...Second sentence."))
            == "First sentence... Second sentence."
        )

    def test_trim_whitespace(self, processor: ErrorProcessor):
        assert (
            processor.trim_whitespace(Line("First sentence.  Second   sentence."))
            == "First sentence. Second sentence."
        )
        assert (
            processor.trim_whitespace(Line("on my part, I mean,  utter idiocy. "))
            == "on my part, I mean, utter idiocy."
        )
        assert processor.trim_whitespace(Line("")) == ""
        assert processor.trim_whitespace(Line(" ")) == ""
        assert processor.trim_whitespace(Line(" ")) == ""
        assert processor.trim_whitespace(Line("test")) == "test"
        assert processor.trim_whitespace(Line(" test")) == "test"
        assert processor.trim_whitespace(Line(" test  ")) == "test"
        assert processor.trim_whitespace(Line("test <i>")) == "test<i>"
        assert processor.trim_whitespace(Line("test </i> ")) == "test</i>"
        assert processor.trim_whitespace(Line("<i>  test")) == "<i>test"
        assert processor.trim_whitespace(Line(" <i>test")) == "<i>test"
        assert processor.trim_whitespace(Line("  <i> test")) == "<i>test"
        assert processor.trim_whitespace(Line("<i>test</i>")) == "<i>test</i>"
        assert processor.trim_whitespace(Line("test test")) == "test test"
        assert processor.trim_whitespace(Line("test  test")) == "test test"
        assert processor.trim_whitespace(Line("test<i>  test")) == "test<i> test"
        assert processor.trim_whitespace(Line("test  <i> test")) == "test <i>test"
        assert (
            processor.trim_whitespace(Line(" test</i><i> </i> ")) == "test</i><i></i>"
        )

    def test_fix_space_punctuation(self, processor: ErrorProcessor):
        assert (
            processor.fix_space_punctuation(
                Line("First sentence  . Second sentence ,  blabla.")
            )
            == "First sentence. Second sentence, blabla."
        )
        assert (
            processor.fix_space_punctuation(Line("First sentence... Second sentence."))
            == "First sentence... Second sentence."
        )
        assert processor.fix_space_punctuation(Line("Whoa ...")) == "Whoa..."
        assert processor.fix_space_punctuation(Line("Whoa...")) == "Whoa..."
        assert (
            processor.fix_space_punctuation(Line("Yeah. ..maybe.")) == "Yeah...maybe."
        )
        assert (
            processor.fix_space_punctuation(Line("Begin... ...end."))
            == "Begin... ...end."
        )
        assert processor.fix_space_punctuation(Line("- ...dialog")) == "- ...dialog"

    def test_fix_hyphen(self, processor: ErrorProcessor):
        assert processor.fix_hyphen(Line("'’")) == "'"

    def test_fix_ampersand(self, processor: ErrorProcessor):
        assert processor.fix_ampersand(Line("&amp;")) == "&"

    def test_fix_quote(self, processor: ErrorProcessor):
        assert processor.fix_quote(Line("&quot;")) == '"'

    def test_fix_music(self, processor: ErrorProcessor):
        assert processor.fix_music(Line("# lalalala")) == "♪ lalalala"

    def test_integration(self, sub_processor: ErrorProcessor):
        output_subtitle = sub_processor.process()
        assert output_subtitle.sections[0].lines == [
            "Madame... ...for you, I'll make it"
        ]
