import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import DialogProcessor, Processor


class TestDialogProcessor:
    @pytest.fixture()
    def processor(self) -> DialogProcessor:
        subtitle: Subtitle = FakeSubtitle()
        processor: Processor = DialogProcessor(subtitle)
        return processor

    def test_clean_dashes(self, processor: DialogProcessor):
        assert processor.clean_dashes("-dialog.") == "- dialog."
        assert processor.clean_dashes("- dialog.") == "- dialog."
        assert processor.clean_dashes("i-in") == "i-in"
        assert processor.clean_dashes("<i>-dialog.</i>") == "<i>- dialog.</i>"
        assert processor.clean_dashes("<i>-</i>dialog.") == "<i>- </i>dialog."
