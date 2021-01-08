#!/usr/bin/env python3
import logging
import os
import sys
from typing import List, Optional

ENCODINGS = [
    "utf-8-sig",
    "iso-8859-1",
]


class Subtitle:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.encoding: Optional[str] = self.load()
        self.file: List[str]
        self.sections: List[SrtSection] = []

    def load(self) -> Optional[str]:
        for e in ENCODINGS:
            try:
                with open(self.filepath, "r", encoding=e) as f:
                    f.readlines()
                    f.seek(0)
                    return e
            except UnicodeDecodeError:
                print("UnicodeDecodeError for encoding %s" % e)
        return None

    def parse(self):
        pass

    def print(self):
        for section in self.sections:
            print(section)


class SrtSectionTiming:
    def __init__(self, start_time: str, end_time: str):
        self.start_time = start_time
        self.end_time = end_time


class SrtSection:
    def __init__(self, timing: SrtSectionTiming, lines: Optional[List[str]] = None):
        self.timing: SrtSectionTiming = timing
        self.lines: List[str] = lines if lines is not None else []

    def add_line(self, line: str):
        self.lines.append(line)

    def __repr__(self):
        text = "\n".join(self.lines)
        return f"{self.timing.start_time}, {self.timing.end_time}\n{text}\n"


class SrtSubtitle(Subtitle):
    def __init__(self, filepath):
        super().__init__(filepath)

    def parse_timing(self, input: str) -> SrtSectionTiming:
        start_time, end_time = input.split(" --> ")
        return SrtSectionTiming(start_time, end_time)

    def parse(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            in_f = [line.strip() for line in f]

        section: SrtSection = None
        for line in in_f:
            # this is index number
            if line.isdigit():
                pass
            # this is timing
            elif " --> " in line:
                timing = self.parse_timing(line)
                section = SrtSection(timing)
            # empty line, that means end of a block
            elif not line:
                self.sections.append(section)
            # so this must be text
            else:
                if len(line) < 1:
                    print("ERROR empty line")
                    continue
                section.add_line(line)


class SubtitleParser:
    SUPPORTED_FORMATS = [".srt"]

    def load(self, filepath) -> Subtitle:
        fname, fext = os.path.splitext(filepath)
        if fext not in self.SUPPORTED_FORMATS:
            raise NotImplementedError
        if fext == ".srt":
            print(f"importing subtitle {filepath}")
            return SrtSubtitle(filepath)
        sys.exit()


FILE = "sub.srt"
parser = SubtitleParser()
subtitle: Subtitle = parser.load(FILE)
subtitle.parse()
subtitle.print()
