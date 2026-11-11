import logging
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass

from subclean import text
from subclean.cue import Cue
from subclean.processors.base import LineProcessor, Processor
from subclean.processors.blacklist import Blacklist
from subclean.processors.fixes import Dialog, Error, Style
from subclean.processors.line_length import LineLength
from subclean.processors.sdh import SDH

__all__ = [
    "PROCESSORS",
    "SDH",
    "Blacklist",
    "Dialog",
    "Error",
    "LineLength",
    "LineProcessor",
    "Options",
    "Processor",
    "Style",
    "build",
    "prune",
    "run",
]

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class Options:
    extra_patterns: tuple[str, ...] = ()
    max_line_length: int = 50


type Factory = Callable[[Options], Processor]

# insertion order is the default pipeline order
PROCESSORS: dict[str, Factory] = {
    "Blacklist": lambda o: Blacklist.with_extra(*o.extra_patterns),
    "SDH": lambda _: SDH(),
    "Dialog": lambda _: Dialog(),
    "Error": lambda _: Error(),
    "LineLength": lambda o: LineLength(o.max_line_length),
    "Style": lambda _: Style(),
}


def build(names: Iterable[str], options: Options) -> list[tuple[str, Processor]]:
    return [(name, PROCESSORS[name](options)) for name in names]


def prune(cues: Iterable[Cue]) -> list[Cue]:
    pruned = (
        cue.with_lines(line for line in cue.lines if text.strip(line)) for cue in cues
    )
    return [cue for cue in pruned if not cue.is_empty()]


def run(cues: Sequence[Cue], processors: Iterable[tuple[str, Processor]]) -> list[Cue]:
    result = list(cues)
    for name, processor in processors:
        logger.info("Running %s", name)
        result = prune(processor(result))
    return result
