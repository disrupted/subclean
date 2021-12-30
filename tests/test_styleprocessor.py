import pytest

from subclean.core.line import Line
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import StyleProcessor
from tests.utils import FakeSubtitle


class TestStyleProcessor:
    @pytest.fixture()
    def processor(self) -> StyleProcessor:
        subtitle: Subtitle = FakeSubtitle()
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
