from pathlib import Path
from typing import Callable

from loguru import logger

from subclean.core.subtitle import Subtitle, SubtitleFormat


class SubtitleParser:
    @staticmethod
    def load(path: Path) -> Subtitle:
        if path.suffix not in SubtitleFormat.values():
            raise NotImplementedError
        logger.info("Importing subtitle {}", path)
        handler: Callable = SubtitleFormat.get_handler(path.suffix)
        subtitle: Subtitle = handler(path)
        return subtitle
