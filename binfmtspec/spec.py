from binfmtspec.line import *
from binfmtspec.renderer import *
from binfmtspec.types import *
from binfmtspec.util import *
from typing import List

class BinarySpec(object):
    positions: List[BinarySpecItem]
    recursion_detection: List[int]

    current_position: int

    scope_line: BinarySpecLine
    variable_line: BinarySpecLine
    repeat_line: BinarySpecLine
    option_line: BinarySpecLine

    variable_count: int
    byte_offset: int

    used_vars: List[str]

    def __init__(self):
        self.positions = []
        self.recursion_detection = []
        self.current_position = 1
        self.variable_count = 0
        self.used_vars = []
        
        self.scope_line = BinarySpecLine("scope")
        self.variable_line = BinarySpecLine("variable")
        self.repeat_line = BinarySpecLine("loop")
        self.option_line = BinarySpecLine("optional")
        self.start_items = []
        self.byte_offset = 1

    def add_bytes(self, count: int):
        for i in range(count):
            self.positions.append({
                "start": self.current_position,
                "length": 1,
                "text": str(self.current_position - self.byte_offset)
            })
            self.current_position += 1

    def add_recursive(self):
        self.positions.append({
            "start": self.current_position,
            "length": 1,
            "text": "..."
        })
        self.current_position += 1
        self.byte_offset += 1

    def rename_level(self, level: int, text: str):
        self.scope_line.rename_level(level, text)

    def render(self, options: BinarySpecRendererOptions):

        final_options: BinarySpecRendererOptions = {
            "font_size": options["font_size"] if "font_size" in options else 15,
            "font_family": options["font_family"] if "font_family" in options else "arial.ttf",
        }

        renderer = BinarySpecImgRenderer(self.positions, [
            self.scope_line,
            self.variable_line,
            self.option_line,
            self.repeat_line,
        ], self.current_position, final_options)

        return renderer.render()

    def start_var(self, name: str = None):
        if name:
            if name in self.used_vars:
                start_idx = 1
                var_name = name + "_{}".format(start_idx)
                while var_name in self.used_vars:
                    start_ids += 1
                    var_name = name + "_{}".format(start_idx)
            else:
                var_name = name
        else:
            var_name = get_variable_name_from_int(self.variable_count)

        self.used_vars.append(var_name)

        self.variable_count += 1
        self.variable_line.open_scope("={}".format(var_name), self.current_position)
        return var_name

    def end_var(self):
        self.variable_line.close_scope(self.current_position)

    def start_scope(self, name: str):
        self.scope_line.open_scope(name, self.current_position)

    def end_scope(self):
        self.scope_line.close_scope(self.current_position)

    def start_repeat(self, count: str):
        self.repeat_line.open_scope("\u00D7[{}]".format(count), self.current_position)

    def end_repeat(self):
        self.repeat_line.close_scope(self.current_position)

    def start_conditional(self, condition: str):
        if "=" not in condition and ">" not in condition and "<" not in condition:
            raise "you have to use = or < or > in the condition"
        self.option_line.open_scope(condition, self.current_position)

    def end_conditional(self):
        self.option_line.close_scope(self.current_position)

    def start_rcd(self, rcd_id: int):
        res = rcd_id in self.recursion_detection
        self.recursion_detection.append(rcd_id)
        return res

    def end_rcd(self):
        self.recursion_detection.pop()