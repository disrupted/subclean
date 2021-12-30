from pathlib import Path

import pytest

from subclean.core.line import Line
from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import SDHProcessor
from tests.utils import FakeSubtitle


class TestSDHProcessor:
    @pytest.fixture()
    def fake_processor(self) -> SDHProcessor:
        subtitle: Subtitle = FakeSubtitle()
        return SDHProcessor(subtitle)

    @pytest.fixture()
    def sub_processor(self) -> SDHProcessor:
        subtitle = SubtitleParser.load(Path("tests/resources/sub_sdh.srt"))
        return SDHProcessor(subtitle)

    def test_is_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.is_hi(Line("[camera shutter]"))
        assert fake_processor.is_hi(Line("-[camera shutter]"))
        assert fake_processor.is_hi(Line("-  [camera shutter]"))
        assert fake_processor.is_hi(Line("(distant shouting))"))
        assert fake_processor.is_hi(Line("[ distant shouting ]"))
        assert fake_processor.is_hi(Line("♪"))
        assert fake_processor.is_hi(Line("- ♪ ♪"))
        assert fake_processor.is_hi(Line("(distant shouting,")) is False
        assert fake_processor.is_hi(Line("weapons clashing))")) is False
        assert fake_processor.is_hi(Line("-[journalists] Christine!")) is False
        assert fake_processor.is_hi(Line("- TAMIKA: Yeah.")) is False
        assert fake_processor.is_hi(Line("♪ (SOFT PIANO MUSIC PLAYS)) ♪"))

    def test_contains_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.contains_hi(Line("that's for you. [sighs]"))
        assert fake_processor.contains_hi(Line("‐TEACHER: blabla..."))
        assert fake_processor.contains_hi(Line("[Laura] sentence"))
        assert fake_processor.contains_hi(Line("<i>[Laura]</i> <i>sentence</i>"))
        assert fake_processor.contains_hi(Line("- CHRISTOPHER:<i> Hello?</i>"))
        assert not fake_processor.contains_hi(Line("9:17 a.m., to be specific,"))

    def test_clean_hi(self, fake_processor: SDHProcessor):
        assert (
            fake_processor.clean_hi(Line("that's for you. [sighs]"))
            == "that's for you. "
        )
        assert fake_processor.clean_hi(Line("‐TEACHER: blabla...")) == "‐blabla..."
        assert fake_processor.clean_hi(Line("[Laura] sentence")) == "sentence"
        assert (
            fake_processor.clean_hi(Line("<i>[Laura]</i> <i>sentence</i>"))
            == "<i></i> <i>sentence</i>"
        )
        assert (
            fake_processor.clean_hi(Line("- CHRISTOPHER:<i> Hello?</i>"))
            == "- <i>Hello?</i>"
        )
        assert (
            fake_processor.clean_hi(Line("9:17 a.m., to be specific,"))
            == "9:17 a.m., to be specific,"
        )

    def test_clean_parentheses(self, fake_processor: SDHProcessor):
        assert (
            fake_processor.clean_parentheses(Line("that's for you. [sighs]"))
            == "that's for you. "
        )
        assert (
            fake_processor.clean_parentheses(
                Line("on my part, I mean, [laughs] utter idiocy.")
            )
            == "on my part, I mean,  utter idiocy."
        )
        assert (
            fake_processor.clean_parentheses(
                Line(
                    "telling a joke [laughs], I mean, [continues laughing] you should've seen him."
                )
            )
            == "telling a joke , I mean,  you should've seen him."
        )

    def test_is_simple_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.is_simple_hi(Line("♪"))
        assert fake_processor.is_simple_hi(Line("- ♪ ♪"))

    def test_is_parentheses(self, fake_processor: SDHProcessor):
        assert fake_processor.is_parentheses(Line("(distant shouting))"))
        assert fake_processor.is_parentheses(Line("[ distant shouting ]"))
        assert fake_processor.is_parentheses(Line("-[camera shutter]"))
        assert fake_processor.is_parentheses(Line("(distant shouting,")) is False
        assert fake_processor.is_parentheses(Line("weapons clashing))")) is False
        assert fake_processor.is_parentheses(Line("[laughing nervously]:")) is False

    def test_is_music(self, fake_processor: SDHProcessor):
        assert fake_processor.is_music(Line("♪ ominous music ♪"))
        assert fake_processor.is_music(Line("- ♪ mysterious music ♪"))
        assert fake_processor.is_music(Line("♪ somber music ♪"))
        assert fake_processor.is_music(Line("♪ foreboding music ♪"))
        assert fake_processor.is_music(Line("♪ chilling music ♪"))
        assert fake_processor.is_music(Line("♪ solemn music ♪"))
        assert fake_processor.is_music(Line(" ♪ dramatic music ♪"))
        assert fake_processor.is_music(Line("♪ poignant music ♪"))
        assert fake_processor.is_music(Line("♪ emotional music ♪"))
        assert fake_processor.is_music(Line("♪ uneasy music ♪"))
        assert fake_processor.is_music(Line("♪ harrowing music ♪"))
        assert fake_processor.is_music(Line("♪ sinister music ♪"))
        assert fake_processor.is_music(Line("♪ upbeat music plays ♪"))
        assert fake_processor.is_music(Line("♪ gentle music ♪"))
        assert fake_processor.is_music(Line("♪ light orchestral music ♪"))
        assert fake_processor.is_music(Line("♪ upbeat folk music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ ominous music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ upbeat music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ smooth music playing ♪"))
        assert fake_processor.is_music(Line("♪ dance music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ swelling orchestral music plays ♪"))
        assert fake_processor.is_music(Line("♪ dramatic music playing ♪"))
        assert fake_processor.is_music(Line("♪ upbeat song playing over speakers ♪"))
        assert fake_processor.is_music(Line("♪ upbeat song playing over headphones ♪"))
        assert fake_processor.is_music(Line("♪ soft, dramatic music ♪"))
        assert fake_processor.is_music(Line("♪ soft, stirring music ♪"))
        assert fake_processor.is_music(Line("♪ music intensifies ♪"))
        assert fake_processor.is_music(Line("♪ music swells ♪"))
        assert fake_processor.is_music(Line("♪ dark music swells ♪"))
        assert fake_processor.is_music(Line("♪ dramatic musical sting ♪"))
        assert fake_processor.is_music(Line("♪ uneasy musical crescendo ♪"))
        assert fake_processor.is_music(Line("♪ up‐tempo percussive music playing ♪"))

    def test_delete_empty_section(self, sub_processor: SDHProcessor):
        assert len(sub_processor.subtitle.sections) == 3
        output_subtitle = sub_processor.process()
        assert len(output_subtitle.sections) == 1
