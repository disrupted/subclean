blacklist = [
    r"^[-_–*:.]+$",  # line only consists of weird characters
    r"^\*|\*$",  # starts or ends on *
    r"Addic7ed|Subscene|Podnapisi|Subtitles",
    r"Support us and become VIP member|remove all ads|Advertise your product or brand here|Hier könnte deine Werbung stehen",
    r"\b(rate this subtitle|Help other users to choose the best subtitles|Helfe anderen Usern die besten Untertitel auszuwählen)\b",
    r"Übersetzung:|Untertitel:",
    r"\b((sub(title)?s?|sync(e|')?d?|cleaned|corrected|rip(ped)?|improved|encod|resync|edit|caption|version|provided)(ed|ing)?\b\s((&|and|,)\s)?)+(by|for|at)\b",
    r"www\.|https?:\/\/|\.(org|link|com)",
    r"\[at\]",  # email
    r"WEB[- ]?(DL|Rip)|HDTV|dTV",  # release tags
    r"\bSDH\b|Season\s*\d+[\s-]+Episode\s*\d+|Episode\s+Title",
    r"greetings from roNy|missing words added by",
    r"300MBUNiTED|:{2,}|Free Online Movies|SharePirate.Com|Sub Upload Date|\bSync:",
    r"\b(WARNER BROS|Media Access Group|WGBH)\b",
]
