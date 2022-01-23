from typing import  TypedDict

class BinarySpecStartItem(TypedDict):
    start: int
    text: str

class BinarySpecItem(BinarySpecStartItem):
    length: int

class MultiLevelBinarySpecItem(BinarySpecItem):
    level: int