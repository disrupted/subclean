from __future__ import annotations

import re
from enum import Enum
from typing import Callable

from loguru import logger

from subclean.blacklist import blacklist
from subclean.core.line import Line
from subclean.core.section import Section
from subclean.core.subtitle import Subtitle


class Processor:
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        self.subtitle = subtitle
        self.operations: list[Callable] = []

    def log(self):
        logger.info("{processor} running", processor=self.__class__.__name__)

    def process(self) -> Subtitle:
        self.log()
        for i, section in enumerate(self.subtitle.sections):
            for j, line in enumerate(section.lines):
                for operation in self.operations:
                    line = operation(line)
                self.subtitle.sections[i].lines[j] = line
        return self.subtitle

    def remove_empty_sections(self) -> None:
        self.subtitle.sections = [s for s in self.subtitle.sections if not s.is_empty()]


class BlacklistProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)
        cli_args = kwargs.get("cli_args")
        if cli_args and cli_args.regex:
            self.add_custom_regex(cli_args.regex)

    def clean_section(self, section: Section) -> Section:
        section.lines = [line for line in section.lines if not self.in_blacklist(line)]
        return section

    @staticmethod
    def in_blacklist(line: Line) -> bool:
        for regex in blacklist:
            if re.search(regex, line, flags=re.IGNORECASE):
                return True
        return False

    def add_custom_regex(self, regex: str):
        logger.debug(
            "{processor} Adding custom regular expression: {}",
            regex,
            processor=self.__class__.__name__,
        )
        blacklist.append(regex)

    def process(self) -> Subtitle:
        self.log()
        self.subtitle.sections = [self.clean_section(s) for s in self.subtitle.sections]
        self.remove_empty_sections()
        return self.subtitle


class DialogProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)
        self.operations: list[Callable] = [self.clean_dashes]

    @staticmethod
    def clean_dashes(line: Line) -> Line:
        return line.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ")


class SDHProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)

    @classmethod
    def is_hi(cls, line: Line) -> bool:
        return bool(
            cls.is_simple_hi(line) or cls.is_parentheses(line) or cls.is_music(line)
        )

    @staticmethod
    def is_simple_hi(line: Line) -> bool:
        return bool(
            re.search(r"^[^a-hj-z.,;?!]*$", line)
            and re.search(r"[A-Z]{2,}|(<i>)?[♪]+(<\/i>)?", line)
        )

    @staticmethod
    def is_parentheses(line: Line) -> bool:
        return bool(re.search(r"^([-‐\s<i>]+)?[(\[*][^\)\]]+[)\]*<\/i>]+$", line))

    @staticmethod
    def is_music(line: Line) -> bool:
        return bool(
            re.search(
                r"^[- ♪<i>]*\s?([-‐a-z,]+\s)*\b(music(al)?|song|track)\b\s?(((play|swell)(s|ing)|intensifies|crescendo|sting)|(fades (in|out)))?\b(\s?over\s(headphones|speakers))?[\s♪<\/i>]*$|vocalizing",
                line,
            )
        )

    @staticmethod
    def contains_hi(line: Line) -> bool:
        return bool(
            re.search(
                r"^([-‐\s<i>]+)?((\b[-A-Za-z.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?!\w)|[\[]+.*[\]:]+)(<\/?i>)?([\s])*|\s?[(\[*].*?[)\]*:]+\s?",
                line,
            )
        )

    @classmethod
    def clean_hi(cls, line: Line) -> Line:
        """Clean hearing impaired."""
        line = line.sub(
            r"^([-‐\s<i>]+)?((\b[-A-Za-z.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?!\w)|[\[]+.*[\]:]+)(<\/?i>)?([\s])*",
            r"\1\5",
        )
        line = cls.clean_parentheses(line)
        return line

    @staticmethod
    def is_parenthesis_not_matching(line: Line) -> bool:
        return bool(
            re.search(r"[()\[\]]", line)
            and (
                line.count("(") != line.count(")") or line.count("[") != line.count("]")
            )
        )

    @staticmethod
    def clean_parentheses(line: Line) -> Line:
        """Clean parentheses ()[]."""
        return line.sub(r"[(\[*].*?[)\]*:]+", "")

    @classmethod
    def clean_section(cls, section: Section) -> Section:
        lines: list[Line] = []
        for line in section.lines:
            if cls.is_hi(line) or cls.is_parenthesis_not_matching(line):
                continue
            elif cls.contains_hi(line):
                line = cls.clean_hi(line)
            lines.append(line)
        section.lines = lines
        return section

    def process(self) -> Subtitle:
        self.log()
        # Clean sections
        self.subtitle.sections = [self.clean_section(s) for s in self.subtitle.sections]
        self.remove_empty_sections()
        return self.subtitle


class LineLengthProcessor(Processor):
    line_length = 50

    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)
        cli_args = kwargs.get("cli_args")
        if cli_args and cli_args.line_length:
            logger.debug(
                "{processor} Setting line length to {}",
                cli_args.line_length,
                processor=self.__class__.__name__,
            )
            self.__class__.line_length = cli_args.line_length

    @classmethod
    def is_short(cls, line: Line) -> bool:
        return len(line) < cls.line_length

    @staticmethod
    def split_dialog_chunks(lines: list[Line]) -> list[list[Line]]:
        chunks = []
        i = 1
        while lines:
            if not len(lines) > max(i, 1):
                chunks.append(lines)
                break
            elif lines[i].is_dialog():
                chunks.append(lines[:i])
                lines = lines[i:]
                i = 1
            else:
                i += 1
        return chunks

    @classmethod
    def process_section(cls, section: Section) -> Section:
        if not len(section) > 1:
            return section
        chunks = cls.split_dialog_chunks(section.lines)
        section.lines = []
        for chunk in chunks:
            if not len(chunk) > 1:
                section.lines.append(chunk[0])
            elif cls.is_short(Line.merge(chunk)):
                section.lines.append(Line.merge(chunk))
            else:
                section.lines += chunk
        return section

    def process(self) -> Subtitle:
        self.log()
        self.subtitle.sections = [
            self.process_section(section) for section in self.subtitle.sections
        ]
        return self.subtitle


class ErrorProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)
        self.operations: list[Callable] = [
            self.fix_hyphen,
            self.fix_spaces,
            self.fix_space_punctuation,
            self.trim_whitespace,
            self.fix_ampersand,
            self.fix_quote,
            self.fix_music,
        ]

    @staticmethod
    def fix_spaces(line: Line) -> Line:
        """Add missing spaces between sentences."""
        return line.sub(r"\b([.?!]+)([A-Z][a-z])", r"\1 \2")

    @staticmethod
    def trim_whitespace(line: Line) -> Line:
        """Trim multiple spaces between words, also if there are style tags in between"""
        return line.sub(r"\s+(<\/?i>)*\s*", r" \1").strip()

    @staticmethod
    def fix_space_punctuation(line: Line) -> Line:
        line = line.sub(
            r"(?<!^-)(?<!\.{3})\s+([.,!?]+)", r"\1"
        )  # remove space before punctuation
        line = line.sub(
            r"([.,!?]+)\s{2,}(?!$)", r"\1 "
        )  # fix multiple spaces after punctuation
        return line

    @staticmethod
    def fix_hyphen(line: Line) -> Line:
        return line.sub(r"'’", "'")

    @staticmethod
    def fix_ampersand(line: Line) -> Line:
        return line.sub(r"&amp;", "&")

    @staticmethod
    def fix_quote(line: Line) -> Line:
        return line.sub(r"&quot;", '"')

    @staticmethod
    def fix_music(line: Line) -> Line:
        return line.sub(r"^#\s", "♪ ")


class StyleProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)
        self.operations: list[Callable] = [
            self.fix_styles,
        ]

    @staticmethod
    def fix_styles(line: Line) -> Line:
        """Remove leftover style tags"""
        return line.sub(r"<\/?i>(\s*)<\/?i>", r"\1")


class Processors(Enum):
    def __str__(self) -> str:
        return self.name

    SDH = SDHProcessor
    Dialog = DialogProcessor
    Error = ErrorProcessor
    Blacklist = BlacklistProcessor
    LineLength = LineLengthProcessor
    Style = StyleProcessor


DEFAULT_PROCESSORS = [
    Processors.Blacklist,
    Processors.SDH,
    Processors.Dialog,
    Processors.Error,
    Processors.LineLength,
    Processors.Style,
]
