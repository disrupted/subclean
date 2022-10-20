from unittest.mock import MagicMock

import pytest

from subclean.core.line import Line
from subclean.processors.processor import DialogProcessor


class TestDialogProcessor:
    @pytest.fixture()
    def processor(self) -> DialogProcessor:
        subtitle = MagicMock()
        return DialogProcessor(subtitle)

    def test_clean_dashes(self, processor: DialogProcessor):
        assert processor.clean_dashes(Line("-dialog.")) == "- dialog."
        assert processor.clean_dashes(Line("- dialog.")) == "- dialog."
        assert processor.clean_dashes(Line("i-in")) == "i-in"
        assert processor.clean_dashes(Line("<i>-dialog.</i>")) == "<i>- dialog.</i>"
        assert processor.clean_dashes(Line("<i>-</i>dialog.")) == "<i>- </i>dialog."
        assert processor.clean_dashes(Line("-...dialog.")) == "- ...dialog."
