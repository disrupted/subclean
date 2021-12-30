from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Callable

from loguru import logger

from subclean.core.line import Line
from subclean.core.section import Section, SrtSection
from subclean.core.section.timing import SrtSectionTiming

ENCODINGS = [
    "utf-8-sig",
    "iso-8859-1",
]


class Subtitle:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.encoding: str | None = self.load()
        self.file: list[str]
        self.sections: list[Section] = []
        self.parse()

    def load(self) -> str | None:
        for e in ENCODINGS:
            try:
                with open(self.filepath, encoding=e) as f:
                    f.readlines()
                    f.seek(0)
                    logger.debug("Found suitable encoding {}", e)
                    return e
            except UnicodeDecodeError:
                logger.warning("UnicodeDecodeError for encoding {}", e)
        logger.error("Failed to load file. Couldn't find suitable encoding.")
        return None

    def parse(self):
        pass

    def add_section(self, section: Section):
        self.sections.append(section)

    def pop_section(self, index: int):
        self.sections.pop(index)

    def print(self):
        for section in self.sections:
            print(section)

    def save(self, path: Path | None = None):
        pass


class SrtSubtitle(Subtitle):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

    @staticmethod
    def __parse_timing(input: str) -> SrtSectionTiming:
        start_time, end_time = input.split(" --> ")
        return SrtSectionTiming(start_time, end_time)

    def parse(self):
        with open(self.filepath, encoding=self.encoding) as f:
            lines: list[str] = list(line.strip() for line in f) + [""]

        for line in lines:
            # empty line (end of section) or index number (begin of section)
            if not line or line.isdigit():
                continue
            # timing
            elif " --> " in line:
                timing = self.__parse_timing(line)
                section = SrtSection(
                    timing, lines=[]
                )  #  TODO why is it not working without explicitely passing lines=[]
                self.sections.append(section)
            # content
            else:
                self.sections[-1].add_line(Line(line))

    def save(self, path: Path | None = None):
        if path is None:
            path = self.filepath.with_stem(self.filepath.stem + "_clean")
        logger.info("Saving subtitle {}", path)
        with open(path, "w") as out_f:
            for index, section in enumerate(self.sections, start=1):
                out_f.write(f"{index}\n{section}\n")


class SubtitleFormat(Enum):
    def __init__(self, ext, handler):
        self.ext: str = ext
        self.handler: Callable = handler

    @classmethod
    def get_handler(cls, ext: str) -> Callable:
        return list(e.handler for e in cls if e.ext == ext)[0]

    @classmethod
    def values(cls) -> set[str]:
        return {e.ext for e in cls}

    SRT = (".srt", SrtSubtitle)
