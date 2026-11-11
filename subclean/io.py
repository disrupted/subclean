import logging
from collections.abc import Sequence
from pathlib import Path

from subclean import formats
from subclean.cue import Cue

logger = logging.getLogger(__name__)

ENCODINGS = ("utf-8-sig", "cp1252")


def decode(data: bytes) -> str:
    for encoding in ENCODINGS:
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            logger.debug("Failed to decode as %s", encoding)
        else:
            logger.debug("Decoded as %s", encoding)
            return text
    return data.decode("latin-1")


def load(path: Path) -> list[Cue]:
    logger.info("Loading %s", path)
    return formats.for_path(path).parse(decode(path.read_bytes()))


def save(path: Path, cues: Sequence[Cue]) -> None:
    logger.info("Saving %s", path)
    path.write_text(formats.for_path(path).dump(cues), encoding="utf-8")
