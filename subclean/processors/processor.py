import re
from enum import Enum
from typing import Callable, List

from loguru import logger

from subclean.blacklist import blacklist
from subclean.core.line import Line
from subclean.core.section import Section
from subclean.core.subtitle import Subtitle


class Processor:
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        self.subtitle = subtitle
        self.operations: List[Callable] = []

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

    def in_blacklist(self, line: Line) -> bool:
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
        self.operations: List[Callable] = [self.clean_dashes]

    @classmethod
    def clean_dashes(cls, line: Line) -> Line:
        return line.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ")


class SDHProcessor(Processor):
    def __init__(self, subtitle: Subtitle, *args, **kwargs):
        super().__init__(subtitle, *args, **kwargs)

    @classmethod
    def is_hi(cls, line: Line) -> bool:
        return bool(
            cls.is_simple_hi(line) or cls.is_parentheses(line) or cls.is_music(line)
        )

    @classmethod
    def is_simple_hi(cls, line: Line) -> bool:
        return bool(
            re.search(r"^[^a-hj-z.,;?!]*$", line)
            and re.search(r"[A-Z]{2,}|(<i>)?[♪]+(<\/i>)?", line)
        )

    @classmethod
    def is_parentheses(cls, line: Line) -> bool:
        return bool(re.search(r"^([-‐\s<i>]+)?[(\[*][^\)\]]+[)\]*<\/i>]+$", line))

    @classmethod
    def is_music(cls, line: Line) -> bool:
        return bool(
            re.search(
                r"^[- ♪]+\s?([-‐a-z,]+\s)*\b(music(al)?|song|track)\b\s?(((play|swell)(s|ing)|intensifies|crescendo|sting))?\b(\s?over\s(headphones|speakers))?\s?♪$",
                line,
            )
        )

    @classmethod
    def contains_hi(cls, line: Line) -> bool:
        return bool(
            re.search(
                r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?|\s?[(\[*].*?[)\]*:]+\s?",
                line,
            )
        )

    @classmethod
    def clean_hi(cls, line: Line) -> Line:
        """Clean hearing impaired."""
        line = line.sub(
            r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?",
            r"\1",
        )
        line = cls.clean_parentheses(line)
        return line

    @classmethod
    def is_parenthesis_not_matching(cls, line: Line) -> bool:
        return bool(
            re.search(r"[()\[\]]", line)
            and (
                line.count("(") != line.count(")") or line.count("[") != line.count("]")
            )
        )

    @classmethod
    def clean_parentheses(cls, line: Line) -> Line:
        """Clean parentheses ()[]."""
        return line.sub(r"[(\[*].*?[)\]*:]+", "")

    @classmethod
    def clean_section(cls, section: Section) -> Section:
        lines: List[Line] = []
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

    @classmethod
    def split_dialog_chunks(cls, lines: List[Line]) -> List[List[Line]]:
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
        self.operations: List[Callable] = [
            self.fix_hyphen,
            self.fix_spaces,
            self.fix_space_punctuation,
            self.trim_whitespace,
            self.fix_ampersand,
            self.fix_quote,
            self.fix_music,
        ]

    @classmethod
    def fix_spaces(cls, line: Line) -> Line:
        """Add missing spaces between sentences."""
        return line.sub(r"\b([.?!]+)([A-Z][a-z])", r"\1 \2")

    @classmethod
    def trim_whitespace(cls, line: Line) -> Line:
        return line.sub(r"\s+", " ").strip()

    @classmethod
    def fix_space_punctuation(cls, line: Line) -> Line:
        line = line.sub(r"\s+([.,!?]+)", r"\1")  # remove space before punctuation
        line = line.sub(
            r"([.,!?]+)\s{2,}(?!$)", r"\1 "
        )  # fix multiple spaces after punctuation
        return line

    @classmethod
    def fix_hyphen(cls, line: Line) -> Line:
        return line.sub(r"'’", "'")

    @classmethod
    def fix_ampersand(cls, line: Line) -> Line:
        return line.sub(r"&amp;", "&")

    @classmethod
    def fix_quote(cls, line: Line) -> Line:
        return line.sub(r"&quot;", '"')

    @classmethod
    def fix_music(cls, line: Line) -> Line:
        return line.sub(r"^#\s", "♪ ")


class Processors(Enum):
    def __str__(self) -> str:
        return self.name

    SDH = SDHProcessor
    Dialog = DialogProcessor
    Error = ErrorProcessor
    Blacklist = BlacklistProcessor
    LineLength = LineLengthProcessor


DEFAULT_PROCESSORS = [
    Processors.Blacklist,
    Processors.SDH,
    Processors.Dialog,
    Processors.Error,
    Processors.LineLength,
]
