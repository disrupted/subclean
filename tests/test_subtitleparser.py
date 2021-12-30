from pathlib import Path

import pytest

from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import SrtSubtitle, Subtitle


class TestSubtitleParser:
    @pytest.fixture()
    def subtitle(self) -> Subtitle:
        subtitle: Subtitle = SubtitleParser.load(Path("tests/resources/sub.srt"))
        return subtitle

    def test_handler(self, subtitle: Subtitle):
        assert isinstance(subtitle, SrtSubtitle)

    def test_srtparser(self, subtitle: SrtSubtitle):
        assert len(subtitle.sections) == 667
        assert len(subtitle.sections[0].lines) == 1
        assert "NETFLIX" in subtitle.sections[0].lines[0]
        assert len(subtitle.sections[13].lines) == 2
        assert subtitle.sections[13].lines == ["- Are you nervous?", "- A little."]
        assert subtitle.sections[13].timing.start_time == "00:01:29,605"
        assert subtitle.sections[13].timing.end_time == "00:01:31,645"
        assert "Translated by" in subtitle.sections[-1].content()
