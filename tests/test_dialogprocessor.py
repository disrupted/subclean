import pytest

from subclean.core.line import Line
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import DialogProcessor
from tests.utils import FakeSubtitle


class TestDialogProcessor:
    @pytest.fixture()
    def processor(self) -> DialogProcessor:
        subtitle: Subtitle = FakeSubtitle()
        return DialogProcessor(subtitle)

    def test_clean_dashes(self, processor: DialogProcessor):
        assert processor.clean_dashes(Line("-dialog.")) == "- dialog."
        assert processor.clean_dashes(Line("- dialog.")) == "- dialog."
        assert processor.clean_dashes(Line("i-in")) == "i-in"
        assert processor.clean_dashes(Line("<i>-dialog.</i>")) == "<i>- dialog.</i>"
        assert processor.clean_dashes(Line("<i>-</i>dialog.")) == "<i>- </i>dialog."
        assert processor.clean_dashes(Line("-...dialog.")) == "- ...dialog."
