from enum import Enum
import re

from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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


def remove_markdown_block_markers(block: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.CODE:
            block = block.replace("```", "")
            if block.startswith(("\n")):
                block = block.lstrip("\n")
            return block
        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.lstrip(">").lstrip())
            return " ".join(stripped_lines)
        case _:
            return block


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ul_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ol_to_html_node(block)
        case _:
            raise ValueError(f"This blocktype ({block_type}) is not implemented")


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    text = block.lstrip("#").lstrip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> HTMLNode:
    text = block.replace("```", "")
    text = text.lstrip()
    raw_text_node = TextNode(text, TextType.PLAIN)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.lstrip("-").strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def ol_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)
