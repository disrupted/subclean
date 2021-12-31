#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from subclean.cli import parse_args
from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import Processor


def subclean(f: Path, processors: list[type[Processor]], args):
    subtitle: Subtitle = SubtitleParser.load(f)
    for processor in processors:
        subtitle = processor(subtitle, cli_args=args).process()
    if args.overwrite:
        args.output = f
    subtitle.save(args.output)


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<g>{time:HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <lvl>{message}</lvl>",
        level=args.log_level,
    )

    processors: list[type[Processor]] = [
        processor.value for processor in args.processors
    ]
    for f in args.file:
        subclean(Path(f.name), processors, args)


if __name__ == "__main__":
    main()
