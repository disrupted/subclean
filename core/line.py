from __future__ import annotations

import re


class Line(str):
    # def __new__(cls, value, *args, **kwargs):
    #     return super(Line, cls).__new__(cls, value)

    # def __init__(self, value, flags=None):
    #     self.flags = flags

    def __len__(self) -> int:
        return len(str(self.strip_styles()))

    def strip_styles(self) -> Line:
        return self.sub(r"<\/?i>", "")

    def sub(self, regex, replacement: str) -> Line:
        return Line(re.sub(regex, replacement, self))

    def strip(self, chars=None) -> Line:
        return Line(super().strip(chars))

    def is_dialog(self) -> bool:
        return bool(re.search(r"^(<\/?i>)*[-]", self))
