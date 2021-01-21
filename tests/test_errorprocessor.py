import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import ErrorProcessor


class TestErrorProcessor:
    @pytest.fixture()
    def processor(self) -> ErrorProcessor:
        subtitle: Subtitle = FakeSubtitle()
        return ErrorProcessor(subtitle)

    def test_fix_spaces(self, processor: ErrorProcessor):
        assert (
            processor.fix_spaces("First sentence.Second sentence.")
            == "First sentence. Second sentence."
        )
        assert (
            processor.fix_spaces("First sentence...Second sentence.")
            == "First sentence... Second sentence."
        )

    def test_trim_whitespace(self, processor: ErrorProcessor):
        assert (
            processor.trim_whitespace("First sentence.  Second   sentence.")
            == "First sentence. Second sentence."
        )
        assert (
            processor.trim_whitespace("on my part, I mean,  utter idiocy. ")
            == "on my part, I mean, utter idiocy."
        )

    def test_fix_space_punctuation(self, processor: ErrorProcessor):
        assert (
            processor.fix_space_punctuation(
                "First sentence  . Second sentence ,  blabla."
            )
            == "First sentence. Second sentence, blabla."
        )
        assert (
            processor.fix_space_punctuation("First sentence... Second sentence.")
            == "First sentence... Second sentence."
        )
        assert processor.fix_space_punctuation("Whoa ...") == "Whoa..."
        assert processor.fix_space_punctuation("Whoa...") == "Whoa..."

    def test_fix_hyphen(self, processor: ErrorProcessor):
        assert processor.fix_hyphen("'’") == "'"

    def test_fix_ampersand(self, processor: ErrorProcessor):
        assert processor.fix_ampersand("&amp;") == "&"

    def test_fix_quote(self, processor: ErrorProcessor):
        assert processor.fix_quote("&quot;") == '"'

    def test_fix_music(self, processor: ErrorProcessor):
        assert processor.fix_music("# lalalala") == "♪ lalalala"
