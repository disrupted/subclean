# Subclean

> Simple CLI to give you better subtitles in seconds.

Tested with Python 3.8 & 3.9

## Example

```
$ python subclean.py subtitle.srt
13:54:03.864 | INFO | core.parser:load:15 - Importing subtitle subtitle.srt
13:54:03.958 | INFO | core.subtitle:save:81 - Saving subtitle subtitle_clean.srt
```

![before-after](https://github.com/disrupted/subclean/blob/main/docs/img/subclean-diff.png?raw=true)

## Usage

```
subclean.py [-h] [-v] [-o OUTPUT] [--processors {Dialog,SDH,LineLength,Blacklist,Error} [{Dialog,SDH,LineLength,Blacklist,Error} ...]]
                   [--regex REGEX]
                   FILE

positional arguments:
  FILE                  Subtitle file to be processed

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -o OUTPUT, --output OUTPUT
                        Set output filename
  --processors {Dialog,SDH,LineLength,Blacklist,Error} [{Dialog,SDH,LineLength,Blacklist,Error} ...]
                        Processors to run
  --regex REGEX         Add custom regular expression to BlacklistProcessor
```
