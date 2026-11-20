from datetime import datetime
from typing import Generic, List, Optional, TypeAlias, TypeVar, Union

T = TypeVar("T")
Rows: TypeAlias = List[dict]


class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item


def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None


def parse(value: Union[int, str]) -> str:
    return "{} at {}".format(value, datetime.utcnow())
