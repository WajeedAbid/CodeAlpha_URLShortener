from dataclasses import dataclass


@dataclass(frozen=True)
class ShortLink:
    code: str
    original_url: str