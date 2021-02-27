from core.line import Line


class TestLine:
    def test_strip_styles(self):
        assert Line("- <i>It's working.</i>").strip_styles() == "- It's working."

    def test_len(self):
        assert len(Line("- <i>It's working.</i>")) == len("- It's working.")

    def test_is_dialog(self):
        assert Line("- <i>This is a dialog.</i>").is_dialog()
        assert Line("-this is also a dialog").is_dialog()
        assert not Line("not a dialog").is_dialog()
