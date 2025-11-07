from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    sanitized_blocks = []
    for block in blocks:
        sanitized_block = block.strip("\n")
        sanitized_block = sanitized_block.strip()
        if sanitized_block != "":
            sanitized_blocks.append(sanitized_block)

    return sanitized_blocks


def block_to_block_type(block: str) -> BlockType:
    if bool(re.match(r"^#{1,6} .+$", block)):
        return BlockType.HEADING
    multiline = block.split("\n")
    if (
        len(multiline) > 1
        and multiline[0].startswith("```")
        and multiline[-1].startswith("```")
    ):
        return BlockType.CODE
    all_quote = True
    all_ul = True
    all_ol = True
    ol_counter = 1
    for line in multiline:
        if not line.startswith(">"):
            all_quote = False
        if not line.startswith("-"):
            all_ul = False
        if not line.startswith(f"{ol_counter}."):
            all_ol = False
        ol_counter += 1

    if all_quote:
        return BlockType.QUOTE
    if all_ul:
        return BlockType.UNORDERED_LIST
    if all_ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
