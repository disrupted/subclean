import sys
from pathlib import Path

from loguru import logger

from subclean.cli import parse_args
from subclean.core.parser import SubtitleParser
from subclean.core.subtitle import Subtitle
from subclean.processors.processor import Processor


def subclean(f: Path, processors: list[type[Processor]], args):
    subtitle: Subtitle = SubtitleParser.load(f.name)
    for processor in processors:
        subtitle = processor(subtitle, cli_args=args).process()
    if args.overwrite:
        args.output = f.name
    subtitle.save(output_filepath=args.output)


def main():
    args = parse_args()
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
        subclean(f, processors, args)


if __name__ == "__main__":
    main()
