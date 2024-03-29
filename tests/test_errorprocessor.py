import pytest

from subclean.core.line import Line
from subclean.core.subtitle import FakeSubtitle, Subtitle
from subclean.processors.processor import ErrorProcessor


class TestErrorProcessor:
    @pytest.fixture()
    def processor(self) -> ErrorProcessor:
        subtitle: Subtitle = FakeSubtitle()
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

    def test_fix_hyphen(self, processor: ErrorProcessor):
        assert processor.fix_hyphen(Line("'’")) == "'"

    def test_fix_ampersand(self, processor: ErrorProcessor):
        assert processor.fix_ampersand(Line("&amp;")) == "&"

    def test_fix_quote(self, processor: ErrorProcessor):
        assert processor.fix_quote(Line("&quot;")) == '"'

    def test_fix_music(self, processor: ErrorProcessor):
        assert processor.fix_music(Line("# lalalala")) == "♪ lalalala"
