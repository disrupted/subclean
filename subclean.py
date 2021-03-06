#!/usr/bin/env python3
import argparse
import sys
from typing import List

from loguru import logger

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import DEFAULT_PROCESSORS, Processor, Processors


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
    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-o", "--output", type=str, help="Set output filename")
    group.add_argument("--overwrite", action="store_true", help="Overwrite input file")
    argparser.add_argument(
        "--processors",
        nargs="+",
        type=lambda processor: Processors[processor],
        choices=set(Processors),
        help=f"Processors to run (default: {' '.join([processor.name for processor in DEFAULT_PROCESSORS])})",
        default=DEFAULT_PROCESSORS,
    )
    argparser.add_argument(
        "--regex", type=str, help="Add custom regular expression to BlacklistProcessor"
    )
    argparser.add_argument(
        "--line-length",
        type=int,
        help="Maximum total line length when concatenating short lines. (default: 50)",
    )
    args = argparser.parse_args()

    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<g>{time:HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <lvl>{message}</lvl>",
        level=args.log_level,
    )

    subtitle: Subtitle = SubtitleParser.load(args.file.name)
    processors: List[Processor] = [processor.value for processor in args.processors]
    for processor in processors:
        subtitle = processor(subtitle, cli_args=args).process()
    if args.overwrite:
        args.output = args.file.name
    subtitle.save(output_filepath=args.output)


if __name__ == "__main__":
    main()
