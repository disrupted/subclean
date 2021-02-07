import pytest

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import LineLengthProcessor


class TestLineLengthProcessor:
    @pytest.fixture()
    def subtitle(self) -> Subtitle:
        subtitle: Subtitle = SubtitleParser.load("linelength.srt")
        return subtitle

    @pytest.fixture()
    def processor(self, subtitle: Subtitle) -> LineLengthProcessor:
        return LineLengthProcessor(subtitle)

    def test_merge_short_lines(self, processor: LineLengthProcessor):
        assert processor.section_meets_criteria(processor.subtitle.sections[0])
        assert len(processor.subtitle.sections[0].lines) == 2
        section = processor.process_section(processor.subtitle.sections[0])
        assert len(section.lines) == 1
        assert section.lines[0] == "Go on now. What you got?"
        assert not processor.section_meets_criteria(processor.subtitle.sections[1])
        assert processor.section_meets_criteria(processor.subtitle.sections[2])
        assert len(processor.subtitle.sections[2].lines) == 2
        section = processor.process_section(processor.subtitle.sections[2])
        assert len(section.lines) == 1
        assert section.lines[0] == "Let me go! I mean it!"
