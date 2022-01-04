from subclean.core.line import Line


class TestLine:
    def test_strip_styles(self):
        assert Line("- <i>It's working.</i>").strip_styles() == "- It's working."
        assert Line("{\an8}appears at top").strip_styles() == "appears at top"

    def test_len(self):
        assert len(Line("- <i>It's working.</i>")) == len("- It's working.")
        assert len(Line("{\an8}appears at top")) == len("appears at top")
        assert len(
            Line('<i>Previously on <font color="#ffff00">"TV Show"</font>...</i>')
        ) == len('Previously on "TV Show"...')

    def test_strip(self):
        assert Line("").strip() == ""
        assert Line(" ").strip() == ""
        assert Line(" ").strip() == ""
        assert Line("test").strip() == "test"
        assert Line(" test").strip() == "test"
        assert Line(" test  ").strip() == "test"
        assert Line("test <i>").strip() == "test<i>"
        assert Line("<i>  test").strip() == "<i>test"
        assert Line(" <i>test").strip() == "<i>test"
        assert Line("<i>test</i>").strip() == "<i>test</i>"

    def test_is_dialog(self):
        assert Line("- <i>This is a dialog.</i>").is_dialog()
        assert Line("-this is also a dialog").is_dialog()
        assert not Line("not a dialog").is_dialog()
