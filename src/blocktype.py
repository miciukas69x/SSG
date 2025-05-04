from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(block):
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and block[count] == " ":
            return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    all_lines_are_quote = all(line.startswith(">") for line in lines)
    if all_lines_are_quote:
        return BlockType.QUOTE

    all_lines_are_unordered = all(line.startswith("- ") for line in lines)
    if all_lines_are_unordered:
        return BlockType.UNORDERED_LIST

    if all(len(line) >= 3 and line[0].isdigit() and line[1] == "." and line[2] == " " for line in lines):
        expected_number = 1
        for line in lines:
            number_str = ""
            for char in line:
                if char.isdigit():
                    number_str += char
                else:
                    break

            if number_str and int(number_str) == expected_number:
                expected_number += 1
            else:
                break
        else:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH