import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import DialogProcessor, Processor


class TestSubtitleParser:
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
