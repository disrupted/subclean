import pytest

from core.subtitle import FakeSubtitle, Subtitle
from processors.processor import Processor, SDHProcessor


class TestSDHProcessor:
    @pytest.fixture()
    def processor(self) -> SDHProcessor:
        subtitle: Subtitle = FakeSubtitle()
        processor: Processor = SDHProcessor(subtitle)
        return processor

    def test_is_hi(self, processor: SDHProcessor):
        assert processor.is_hi("[camera shutter]")
        assert processor.is_hi("-[camera shutter]")
        assert processor.is_hi("-  [camera shutter]")
        assert processor.is_hi("(distant shouting)")
        assert processor.is_hi("[ distant shouting ]")
        assert processor.is_hi("♪")
        assert processor.is_hi("- ♪ ♪")
        assert processor.is_hi("(distant shouting,") is False
        assert processor.is_hi("weapons clashing)") is False
        assert processor.is_hi("-[journalists] Christine!") is False
        assert processor.is_hi("- TAMIKA: Yeah.") is False
        assert processor.is_hi("♪ (SOFT PIANO MUSIC PLAYS) ♪")

    def test_is_simple_hi(self, processor: SDHProcessor):
        assert processor.is_simple_hi("♪")
        assert processor.is_simple_hi("- ♪ ♪")
        # assert processor.is_simple_hi("[ distant shouting ]")
        # assert processor.is_simple_hi("-[camera shutter]")
        # assert processor.is_simple_hi("(distant shouting,") is False
        # assert processor.is_simple_hi("weapons clashing)") is False
        # assert processor.is_simple_hi("[laughing nervously]:") is False

    def test_is_parentheses(self, processor: SDHProcessor):
        assert processor.is_parentheses("(distant shouting)")
        assert processor.is_parentheses("[ distant shouting ]")
        assert processor.is_parentheses("-[camera shutter]")
        assert processor.is_parentheses("(distant shouting,") is False
        assert processor.is_parentheses("weapons clashing)") is False
        assert processor.is_parentheses("[laughing nervously]:") is False

    def test_is_music(self, processor: SDHProcessor):
        assert processor.is_music("♪ ominous music ♪")
        assert processor.is_music("- ♪ mysterious music ♪")
        assert processor.is_music("♪ somber music ♪")
        assert processor.is_music("♪ foreboding music ♪")
        assert processor.is_music("♪ chilling music ♪")
        assert processor.is_music("♪ solemn music ♪")
        assert processor.is_music(" ♪ dramatic music ♪")
        assert processor.is_music("♪ poignant music ♪")
        assert processor.is_music("♪ emotional music ♪")
        assert processor.is_music("♪ uneasy music ♪")
        assert processor.is_music("♪ harrowing music ♪")
        assert processor.is_music("♪ sinister music ♪")
        assert processor.is_music("♪ upbeat music plays ♪")
        assert processor.is_music("♪ gentle music ♪")
        assert processor.is_music("♪ light orchestral music ♪")
        assert processor.is_music("♪ upbeat folk music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ ominous music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ upbeat music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ smooth music playing ♪")
        assert processor.is_music("♪ dance music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ swelling orchestral music plays ♪")
        assert processor.is_music("♪ dramatic music playing ♪")
        assert processor.is_music("♪ upbeat song playing over speakers ♪")
        assert processor.is_music("♪ upbeat song playing over headphones ♪")
        assert processor.is_music("♪ soft, dramatic music ♪")
        assert processor.is_music("♪ soft, stirring music ♪")
        assert processor.is_music("♪ music intensifies ♪")
        assert processor.is_music("♪ music swells ♪")
        assert processor.is_music("♪ dark music swells ♪")
        assert processor.is_music("♪ dramatic musical sting ♪")
        assert processor.is_music("♪ uneasy musical crescendo ♪")
        assert processor.is_music("♪ up‐tempo percussive music playing ♪")
