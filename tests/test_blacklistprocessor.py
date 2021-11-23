import pytest

from subclean.core.line import Line
from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import FakeSubtitle, Subtitle
from subclean.processors.processor import BlacklistProcessor


class TestBlacklistProcessor:
    @pytest.fixture()
    def fake_processor(self) -> BlacklistProcessor:
        subtitle: Subtitle = FakeSubtitle()
        return BlacklistProcessor(subtitle)

    @pytest.fixture()
    def sub_processor(self) -> BlacklistProcessor:
        subtitle = SubtitleParser.load("sub_ads.srt")
        return BlacklistProcessor(subtitle)

    def test_in_blacklist(self, fake_processor: BlacklistProcessor):
        assert fake_processor.in_blacklist(Line("[http://example.com]"))
        assert fake_processor.in_blacklist(Line("Visit https://another-example.com"))

    def test_process(self, sub_processor: BlacklistProcessor):
        assert len(sub_processor.subtitle.sections) == 2
        output_subtitle = sub_processor.process()
        print(output_subtitle.sections)
        assert len(output_subtitle.sections) == 0
