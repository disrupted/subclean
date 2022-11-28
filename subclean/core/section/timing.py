class SectionTiming:
    def __init__(self, start_time: str, end_time: str) -> None:
        self.start_time: str = start_time
        self.end_time: str = end_time


class SrtSectionTiming(SectionTiming):
    def __str__(self) -> str:
        return f"{self.start_time} --> {self.end_time}"
