from binfmtspec.types import *
from typing import List, Dict

class BinarySpecLine(object):
    items: List[BinarySpecItem]
    scope_items: List[MultiLevelBinarySpecItem]
    level_count: int
    name: str
    rename_map: Dict[int, str]

    def __init__(self, name: str): 
        self.scope_items = []
        self.items = []
        self.level_count = 0
        self.name = name
        self.rename_map = {}

    def open_scope(self, text: str, pos: int):
        self.scope_items.append({
            "start": pos,
            "text": text.replace('\n', ' ').replace('\r', '')
        })
        self.level_count = max(self.level_count, len(self.scope_items))

    def get_start_item(self, line_idx: int):
        if line_idx in self.rename_map:
            text = self.rename_map[line_idx]
        else:
            text = "{} ln. {}".format(self.name, line_idx + 1)

        return {
            "start": 0,
            "length": 1,
            "text": text
        } 

    def rename_level(self, level: int, text: str):
        self.rename_map[level] = text

    def get_start_items(self):
        return [ self.get_start_item(i) for i in range(self.level_count) ]

    def get_level(self, level: int):
        return [ item for item in self.items if item["level"] == level ] + [ self.get_start_item(level) ]

    def close_scope(self, pos: int):
        top_item = self.scope_items.pop()
        self.items.append({
            "start": top_item["start"],
            "text": top_item["text"],
            "level": len(self.scope_items),
            "length": pos - top_item["start"]
        })