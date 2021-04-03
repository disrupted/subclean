from __future__ import annotations

import re


class Line(str):
    def __len__(self) -> int:
        return len(str(self.strip_styles()))

    def strip_styles(self) -> Line:
        return self.sub(r"<[^>]*>", "")

    def sub(self, regex, replacement: str) -> Line:
        return Line(re.sub(regex, replacement, self))

    def strip(self, chars=None) -> Line:
        return Line(super().strip(chars))

    def is_dialog(self) -> bool:
        return bool(re.search(r"^(<\/?i>)*[-]", self))

    @staticmethod
    def merge(lines: list[Line]) -> Line:
        return Line(" ".join(lines))
