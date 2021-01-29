import pytest

from core.parser import SubtitleParser
from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import SDHProcessor


class TestSDHProcessor:
    @pytest.fixture()
    def fake_processor(self) -> SDHProcessor:
        subtitle: Subtitle = FakeSubtitle()
        return SDHProcessor(subtitle)

    @pytest.fixture()
    def sub_processor(self) -> SDHProcessor:
        parser = SubtitleParser()
        subtitle = parser.load("sub_sdh.srt")
        # subtitle.parse()
        return SDHProcessor(subtitle)

    def test_is_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.is_hi("[camera shutter]")
        assert fake_processor.is_hi("-[camera shutter]")
        assert fake_processor.is_hi("-  [camera shutter]")
        assert fake_processor.is_hi("(distant shouting)")
        assert fake_processor.is_hi("[ distant shouting ]")
        assert fake_processor.is_hi("♪")
        assert fake_processor.is_hi("- ♪ ♪")
        assert fake_processor.is_hi("(distant shouting,") is False
        assert fake_processor.is_hi("weapons clashing)") is False
        assert fake_processor.is_hi("-[journalists] Christine!") is False
        assert fake_processor.is_hi("- TAMIKA: Yeah.") is False
        assert fake_processor.is_hi("♪ (SOFT PIANO MUSIC PLAYS) ♪")

    def test_contains_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.contains_hi("that's for you. [sighs]")

    # def test_clean_hi(self, fake_processor: SDHProcessor):
    #     assert fake_processor.clean_hi("that's for you. [sighs]") == "that's for you."

    def test_clean_parentheses(self, fake_processor: SDHProcessor):
        assert (
            fake_processor.clean_parentheses("that's for you. [sighs]")
            == "that's for you. "
        )
        assert (
            fake_processor.clean_parentheses(
                "on my part, I mean, [laughs] utter idiocy."
            )
            == "on my part, I mean,  utter idiocy."
        )
        assert (
            fake_processor.clean_parentheses(
                "telling a joke [laughs], I mean, [continues laughing] you should've seen him."
            )
            == "telling a joke , I mean,  you should've seen him."
        )

    def test_is_simple_hi(self, fake_processor: SDHProcessor):
        assert fake_processor.is_simple_hi("♪")
        assert fake_processor.is_simple_hi("- ♪ ♪")
        # assert fake_processor.is_simple_hi("[ distant shouting ]")
        # assert fake_processor.is_simple_hi("-[camera shutter]")
        # assert fake_processor.is_simple_hi("(distant shouting,") is False
        # assert fake_processor.is_simple_hi("weapons clashing)") is False
        # assert fake_processor.is_simple_hi("[laughing nervously]:") is False

    def test_is_parentheses(self, fake_processor: SDHProcessor):
        assert fake_processor.is_parentheses("(distant shouting)")
        assert fake_processor.is_parentheses("[ distant shouting ]")
        assert fake_processor.is_parentheses("-[camera shutter]")
        assert fake_processor.is_parentheses("(distant shouting,") is False
        assert fake_processor.is_parentheses("weapons clashing)") is False
        assert fake_processor.is_parentheses("[laughing nervously]:") is False

    def test_is_music(self, fake_processor: SDHProcessor):
        assert fake_processor.is_music("♪ ominous music ♪")
        assert fake_processor.is_music("- ♪ mysterious music ♪")
        assert fake_processor.is_music("♪ somber music ♪")
        assert fake_processor.is_music("♪ foreboding music ♪")
        assert fake_processor.is_music("♪ chilling music ♪")
        assert fake_processor.is_music("♪ solemn music ♪")
        assert fake_processor.is_music(" ♪ dramatic music ♪")
        assert fake_processor.is_music("♪ poignant music ♪")
        assert fake_processor.is_music("♪ emotional music ♪")
        assert fake_processor.is_music("♪ uneasy music ♪")
        assert fake_processor.is_music("♪ harrowing music ♪")
        assert fake_processor.is_music("♪ sinister music ♪")
        assert fake_processor.is_music("♪ upbeat music plays ♪")
        assert fake_processor.is_music("♪ gentle music ♪")
        assert fake_processor.is_music("♪ light orchestral music ♪")
        assert fake_processor.is_music("♪ upbeat folk music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ ominous music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ upbeat music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ smooth music playing ♪")
        assert fake_processor.is_music("♪ dance music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ swelling orchestral music plays ♪")
        assert fake_processor.is_music("♪ dramatic music playing ♪")
        assert fake_processor.is_music("♪ upbeat song playing over speakers ♪")
        assert fake_processor.is_music("♪ upbeat song playing over headphones ♪")
        assert fake_processor.is_music("♪ soft, dramatic music ♪")
        assert fake_processor.is_music("♪ soft, stirring music ♪")
        assert fake_processor.is_music("♪ music intensifies ♪")
        assert fake_processor.is_music("♪ music swells ♪")
        assert fake_processor.is_music("♪ dark music swells ♪")
        assert fake_processor.is_music("♪ dramatic musical sting ♪")
        assert fake_processor.is_music("♪ uneasy musical crescendo ♪")
        assert fake_processor.is_music("♪ up‐tempo percussive music playing ♪")

    def test_delete_empty_section(self, sub_processor: SDHProcessor):
        assert len(sub_processor.subtitle.sections) == 3
        output_subtitle = sub_processor.process()
        assert len(output_subtitle.sections) == 1
