from pathlib import Path
from unittest.mock import MagicMock

import pytest

from subclean.core.line import Line
from subclean.core.parser import SubtitleParser
from subclean.processors.processor import BlacklistProcessor


class TestBlacklistProcessor:
    @pytest.fixture()
    def fake_processor(self) -> BlacklistProcessor:
        subtitle = MagicMock()
        return BlacklistProcessor(subtitle)

    @pytest.fixture()
    def sub_processor(self) -> BlacklistProcessor:
        subtitle = SubtitleParser.load(Path("tests/resources/sub_ads.srt"))
        return BlacklistProcessor(subtitle)

    def test_in_blacklist(self, fake_processor: BlacklistProcessor):
        assert fake_processor.in_blacklist(Line("Advertise your product or brand here"))
        assert fake_processor.in_blacklist(Line("contact www.OpenSubtitles.org today"))
        assert fake_processor.in_blacklist(
            Line('<font color="#ffff00">Provided by username</font>')
        )
        assert fake_processor.in_blacklist(Line("[http://example.com]"))
        assert fake_processor.in_blacklist(Line("http://foo.network"))
        assert fake_processor.in_blacklist(Line("Visit https://another-example.com"))
        assert fake_processor.in_blacklist(Line("find more under subs.link"))
        assert fake_processor.in_blacklist(Line("twitter.com/username"))

    def test_process(self, sub_processor: BlacklistProcessor):
        assert len(sub_processor.subtitle.sections) == 3
        output_subtitle = sub_processor.process()
        assert len(output_subtitle.sections) == 0
