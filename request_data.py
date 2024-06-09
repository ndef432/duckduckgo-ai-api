import dataclasses
from typing import Self


@dataclasses.dataclass
class RequestData:
    url: str
    headers: dict[str, str]
    body: str | None

    @classmethod
    def from_dict(cls, src: dict) -> Self:
        return cls(src['url'], src['headers'], src.get('body'))
