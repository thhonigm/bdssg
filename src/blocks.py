import re

class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = []
    block = []
    for line in markdown.split("\n"):
        line = line.strip()
        if line == "":
            if len(block) > 0:
                blocks.append("\n".join(block))
                block = []
        else:
            block.append(line)
    if len(block) > 0:
        blocks.append("\n".join(block))
    return blocks

block_type_re = {
    BlockType.HEADING: re.compile("#{1,6} "),
    BlockType.CODE: re.compile("```.*```$", re.DOTALL),
}

block_lines_type_re = {
    BlockType.QUOTE: re.compile(r"(>) "),
    BlockType.UNORDERED_LIST: re.compile(r"([-*]) "),
    BlockType.ORDERED_LIST: re.compile(r"([0-9]?)\. "),
}

def next_start(block_type, prev_start, this_start):
    match block_type:
        case BlockType.UNORDERED_LIST:
            if prev_start is None:
                return True, this_start
            return prev_start == this_start, prev_start
        case BlockType.ORDERED_LIST:
            try:
                this_start = int(this_start)
                return prev_start == this_start, this_start + 1
            except ValueError:
                pass
            return False, prev_start + 1
        case default:
            return True, None

def block_to_block_type(block):
    for t in block_type_re:
        if block_type_re[t].match(block):
            return t
    for t in block_lines_type_re:
        start = 1 if t == BlockType.ORDERED_LIST else None
        for l in block.split("\n"):
            m = block_lines_type_re[t].match(l)
            if not m:
                break
            ok, start = next_start(t, start, m.group(1))
            if not ok:
                break
        else:
            return t
    return BlockType.PARAGRAPH

