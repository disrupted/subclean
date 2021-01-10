import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import DialogProcessor, ErrorProcessor, Processor


class TestDialogProcessor:
    @pytest.fixture()
    def processor(self):
        subtitle: Subtitle = FakeSubtitle()
        processor: Processor = DialogProcessor(subtitle)
        return processor

    def test_clean_dashes(self, processor):
        assert processor.clean_dashes("-dialog.") == "- dialog."
        assert processor.clean_dashes("- dialog.") == "- dialog."
        assert processor.clean_dashes("i-in") == "i-in"
        assert processor.clean_dashes("<i>-dialog.</i>") == "<i>- dialog.</i>"
        assert processor.clean_dashes("<i>-</i>dialog.") == "<i>- </i>dialog."


class TestErrorProcessor:
    @pytest.fixture()
    def processor(self):
        subtitle: Subtitle = FakeSubtitle()
        processor: Processor = ErrorProcessor(subtitle)
        return processor

    def test_fix_spaces(self, processor: Processor):
        assert (
            processor.fix_spaces("First sentence.Second sentence.")
            == "First sentence. Second sentence."
        )

    def test_trim_whitespace(self, processor: Processor):
        assert (
            processor.trim_whitespace("First sentence.  Second sentence.")
            == "First sentence. Second sentence."
        )

    def test_fix_hyphen(self, processor: Processor):
        assert processor.fix_hyphen("'’") == "'"

    def test_fix_ampersand(self, processor: Processor):
        assert processor.fix_ampersand("&amp;") == "&"

    def test_fix_quote(self, processor: Processor):
        assert processor.fix_quote("&quot;") == '"'

    def test_fix_music(self, processor: Processor):
        assert processor.fix_music("# lalalala") == "♪ lalalala"
