#!/usr/bin/env python3
import argparse
import sys

from loguru import logger

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import Processors

DEFAULT_PROCESSORS = [
    Processors.Blacklist,
    Processors.SDH,
    Processors.Dialog,
    Processors.Error,
    Processors.LineLength,
]


def main():
    argparser = argparse.ArgumentParser(description="Clean Subtitles")
    argparser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("r"),
        help="Subtitle file to be processed",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        help="Increase output verbosity",
        dest="log_level",
        const="DEBUG",
        default="INFO",
    )
    argparser.add_argument("-o", "--output", type=str, help="Set output filename")
    argparser.add_argument(
        "--processors",
        nargs="+",
        type=lambda processor: Processors[processor],
        choices=set(Processors),
        help="Processors to run",
        default=DEFAULT_PROCESSORS,
    )
    argparser.add_argument(
        "--regex", type=str, help="Add custom regular expression to BlacklistProcessor"
    )
    argparser.add_argument(
        "--line-length", type=int, help="Concat lines shorter than x"
    )
    args = argparser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.log_level)

    subtitle: Subtitle = SubtitleParser.load(args.file.name)
    processors = [processor.value for processor in args.processors]
    for processor in processors:
        subtitle = processor(subtitle, cli_args=args).process()
    subtitle.save(output_filepath=args.output)


if __name__ == "__main__":
    main()
