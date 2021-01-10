import re

from core.subtitle import Subtitle


class Processor:
    def __init__(self, subtitle: Subtitle):
        self.subtitle = subtitle

    def process(self):
        pass


class DialogProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)

    def clean_dashes(self, line: str) -> str:
        return re.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ", line)

    def process(self) -> Subtitle:
        for i, section in enumerate(self.subtitle.sections):
            for j, line in enumerate(section.lines):
                self.subtitle.sections[i].lines[j] = self.clean_dashes(line)
        return self.subtitle
