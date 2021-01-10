import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import ErrorProcessor, Processor


class TestErrorProcessor:
    @pytest.fixture()
    def processor(self) -> ErrorProcessor:
        subtitle: Subtitle = FakeSubtitle()
        processor: Processor = ErrorProcessor(subtitle)
        return processor

    def test_fix_spaces(self, processor: ErrorProcessor):
        assert (
            processor.fix_spaces("First sentence.Second sentence.")
            == "First sentence. Second sentence."
        )

    def test_trim_whitespace(self, processor: ErrorProcessor):
        assert (
            processor.trim_whitespace("First sentence.  Second sentence.")
            == "First sentence. Second sentence."
        )

    def test_fix_hyphen(self, processor: ErrorProcessor):
        assert processor.fix_hyphen("'’") == "'"

    def test_fix_ampersand(self, processor: ErrorProcessor):
        assert processor.fix_ampersand("&amp;") == "&"

    def test_fix_quote(self, processor: ErrorProcessor):
        assert processor.fix_quote("&quot;") == '"'

    def test_fix_music(self, processor: ErrorProcessor):
        assert processor.fix_music("# lalalala") == "♪ lalalala"
