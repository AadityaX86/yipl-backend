import re
_ISBN10_RE = re.compile(r"^\d{10}$")
def is_valid_isbn10(v: str) -> bool: return bool(_ISBN10_RE.fullmatch(v or ""))
def is_valid_year(v: int | None) -> bool: return v is None or 1000 <= int(v) <= 2100
