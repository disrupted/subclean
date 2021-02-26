import processors.utils as utils


def test_remove_styles():
    assert utils.remove_styles("- <i>It's working.</i>") == "- It's working."
