from pathlib import Path
from typing import Callable

from loguru import logger

from subclean.core.subtitle import Subtitle, SubtitleFormat


class SubtitleParser:
    @staticmethod
    def load(filepath: str) -> Subtitle:
        p = Path(filepath)
        if p.suffix not in SubtitleFormat.values():
            raise NotImplementedError
        logger.info("Importing subtitle {}", filepath)
        handler: Callable = SubtitleFormat.get_handler(p.suffix)
        subtitle: Subtitle = handler(filepath)
        return subtitle
