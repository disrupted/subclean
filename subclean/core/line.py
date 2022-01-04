from __future__ import annotations

import re


class Line(str):
    def __len__(self) -> int:
        return len(str(self.strip_styles()))

    def strip_styles(self) -> Line:
        return self.sub(r"<[^>]*>", "").sub(r"{[^}]*}", "")

    def sub(self, regex, replacement: str) -> Line:
        return Line(re.sub(regex, replacement, self))

    def strip(self, chars=None) -> Line:
        """Remove leading and trailing whitespace
        also between style tags"""
        return self.sub(r"^(<\/?i>)*\s+|\s+(<\/?i>)*$", r"\1\2")

    def is_dialog(self) -> bool:
        return bool(re.search(r"^(<\/?i>)*[-]", self))

    @staticmethod
    def merge(lines: list[Line]) -> Line:
        return Line(" ".join(lines))
