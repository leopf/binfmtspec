from binfmtspec.line import *
from binfmtspec.types import *
from typing import List
from PIL import ImageFont, ImageDraw, Image
import math

class BinarySpecImgRenderer(object):
    lines: List[BinarySpecLine]
    positions: List[BinarySpecItem]
    font_size: float

    row_height: int
    table_width: int

    column_starts: List[int]
    column_count: int
    
    def __init__(self, positions: List[BinarySpecItem], lines: List[BinarySpecLine], column_count: int, font_size: float):
        self.font_size = font_size
        self.positions = positions
        self.lines = lines
        self.column_count = column_count
        self.row_height = 0
        self.column_starts = list([ 0 for _ in range(self.column_count + 1) ])

    def measure_cell_dims(self, font: ImageFont):
        items = self.get_all_items()
        column_widths: List[int] = list([ 0 for _ in range(self.column_count) ])

        for item in items:
            item_text_width, item_text_height = font.getsize(item["text"])
            item_width = item_text_width + 20
            cell_width = math.ceil(item_width / item["length"])

            self.row_height = max(math.ceil(item_text_height + 20), self.row_height)

            for i in range(item["start"], item["start"] + item["length"]):
                column_widths[i] = max(column_widths[i], cell_width)

        self.table_width = sum(column_widths) + 1

        current_x = 0
        for i in range(self.column_count):
            self.column_starts[i] = current_x
            current_x += column_widths[i]

        self.column_starts[-1] = current_x

    def get_all_items(self):
        return self.get_start_items() + sum([ line.items for line in self.lines ], []) + self.positions

    def get_start_items(self):
        return sum([ line.get_start_items() for line in self.lines ], [])

    def draw_item(self, item: BinarySpecItem, row_idx: int, draw: ImageDraw, font: ImageFont):
        box_y = row_idx * self.row_height
        box_y_end = box_y + self.row_height
        box_x = self.column_starts[item["start"]]
        box_x_end = self.column_starts[item["start"] + item["length"]]

        box_w = box_x_end - box_x
        box_h = box_y_end - box_y

        item_text_width, item_text_height = font.getsize(item["text"])

        box_x_offset = math.floor((box_w - item_text_width) / 2)
        box_y_offset = math.floor((box_h - item_text_height) / 2)

        draw.text((box_x + box_x_offset, box_y + box_y_offset), item["text"], font=font, fill=0x000000) 

        draw.line([ box_x, box_y, box_x, box_y_end ], fill=0x000000, width=1)
        draw.line([ box_x_end, box_y, box_x_end, box_y_end ], fill=0x000000, width=1)

    def draw_row_seperator(self, draw: ImageDraw, row_idx: int):
        box_y = row_idx * self.row_height
        draw.line([ 0, box_y, self.table_width - 1, box_y ], fill=0x000000, width=1)

    def render(self):
        font = ImageFont.truetype("arial.ttf", self.font_size)
        self.measure_cell_dims(font)

        row_count = 1 + sum([ line.level_count for line in self.lines ])
        table_height = row_count * self.row_height + 1

        img = Image.new(mode="RGB", size=(self.table_width, table_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        row_idx = 0
        self.draw_row_seperator(draw, row_idx)
        for item in self.positions:
            self.draw_item(item, row_idx, draw, font)

        row_idx += 1
        self.draw_row_seperator(draw, row_idx)

        for line in self.lines:
            for level in range(line.level_count):
                for item in line.get_level(level):
                    self.draw_item(item, row_idx, draw, font)
                row_idx += 1
                self.draw_row_seperator(draw, row_idx)

        draw.line([ 0, 0, 0, table_height - 1 ], fill=0x000000, width=1)
        draw.line([ self.table_width - 1, 0, self.table_width - 1, table_height - 1 ], fill=0x000000, width=1)

        return img