from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from subclean.cue import Cue
from subclean.formats.srt import SrtFormat


class SubtitleFormat(Protocol):
    def parse(self, text: str, /) -> list[Cue]: ...

    def dump(self, cues: Sequence[Cue], /) -> str: ...


class UnsupportedFormatError(ValueError):
    def __init__(self, path: Path) -> None:
        supported = ", ".join(FORMATS)
        super().__init__(
            f"Unsupported subtitle format {path.suffix!r} (supported: {supported})"
        )


FORMATS: dict[str, SubtitleFormat] = {".srt": SrtFormat()}


def for_path(path: Path) -> SubtitleFormat:
    try:
        return FORMATS[path.suffix.lower()]
    except KeyError:
        raise UnsupportedFormatError(path) from None
