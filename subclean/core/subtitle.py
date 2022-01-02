from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Callable

from loguru import logger

from subclean.core.line import Line
from subclean.core.section import Section, SrtSection
from subclean.core.section.timing import SrtSectionTiming


class Encoding(Enum):
    UTF_8_SIG = "utf-8-sig"
    ISO_8859_1 = "iso-8859-1"
    NONE = None


class Subtitle:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.encoding: Encoding = self.load()
        self.file: list[str]
        self.sections: list[Section] = []
        self.parse()

    def load(self) -> Encoding:
        for e in Encoding:
            try:
                with open(self.filepath, encoding=e.value) as f:
                    f.read()
                    f.seek(0)
                    logger.debug("Found suitable encoding {}", e)
                    return e
            except UnicodeDecodeError:
                logger.warning("UnicodeDecodeError for encoding {}", e)
        logger.error("Failed to load file. Couldn't find suitable encoding.")
        return Encoding.NONE

    def parse(self):
        raise NotImplementedError

    def add_section(self, section: Section):
        self.sections.append(section)

    def pop_section(self, index: int):
        self.sections.pop(index)

    def print(self):
        for section in self.sections:
            print(section)

    def read(self):
        with open(self.filepath, encoding=self.encoding.value) as f:
            for line in f:
                yield line.strip()
        yield ""  # append empty new line

    def save(self, path: Path | None = None):
        raise NotImplementedError


class SrtSubtitle(Subtitle):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

    @staticmethod
    def __parse_timing(input: str) -> SrtSectionTiming:
        start_time, end_time = input.split(" --> ")
        return SrtSectionTiming(start_time, end_time)

    def parse(self):
        for line in self.read():
            # empty line (end of section) or index number (begin of section)
            if not line or line.isdigit():
                continue
            # timing
            elif " --> " in line:
                timing = self.__parse_timing(line)
                section = SrtSection(timing)
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
