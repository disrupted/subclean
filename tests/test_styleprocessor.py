from unittest.mock import MagicMock

import pytest

from subclean.core.line import Line
from subclean.processors.processor import StyleProcessor


class TestStyleProcessor:
    @pytest.fixture()
    def processor(self) -> StyleProcessor:
        subtitle = MagicMock()
        return StyleProcessor(subtitle)

    def test_fix_styles(self, processor: StyleProcessor):
        assert processor.fix_styles(Line("<i></i>")) == ""
        assert processor.fix_styles(Line("<i> </i>")) == " "
        assert processor.fix_styles(Line("</i> <i>")) == " "
        assert processor.fix_styles(Line("<i></i><i></i>")) == ""
        assert (
            processor.fix_styles(Line("<i></i> <i> </i> <i>sentence</i>"))
            == "   <i>sentence</i>"
        )
