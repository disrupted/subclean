import shutil
from pathlib import Path

import pytest

from subclean.cli import main

SUBS = Path(__file__).parent / "subs"


@pytest.mark.parametrize(
    "input_path", sorted(SUBS.glob("*.input.srt")), ids=lambda p: p.name
)
def test_reference_output(input_path: Path, tmp_path: Path) -> None:
    ref_path = input_path.with_name(input_path.name.replace(".input.", ".ref."))
    output = tmp_path / "out.srt"
    main([str(input_path), "-o", str(output)])
    assert output.read_text() == ref_path.read_text()


def test_default_output_path(tmp_path: Path) -> None:
    source = tmp_path / "movie.srt"
    shutil.copy(SUBS.parent / "resources" / "sub_ads.srt", source)
    main([str(source)])
    assert (tmp_path / "movie_clean.srt").exists()


def test_overwrite(tmp_path: Path) -> None:
    source = tmp_path / "movie.srt"
    shutil.copy(SUBS.parent / "resources" / "sub_ads.srt", source)
    main([str(source), "--overwrite"])
    assert source.read_text() == ""


def test_output_requires_single_file(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        main(["a.srt", "b.srt", "-o", str(tmp_path / "out.srt")])


def test_unsupported_format_fails(tmp_path: Path) -> None:
    source = tmp_path / "movie.ass"
    source.write_text("")
    with pytest.raises(SystemExit, match="1"):
        main([str(source)])
