from pathlib import Path

from subclean.subclean import main


class TestIntegration:
    def test_integration(self):
        for input_path in Path("tests/subs").glob("*.input.srt"):
            ref_path = input_path.with_suffix("").with_suffix(".ref.srt")
            result_path = input_path.with_stem(input_path.stem + "_clean")
            try:
                # run subclean
                main([str(input_path)])
                assert result_path.read_text() == ref_path.read_text()
            finally:
                result_path.unlink()
