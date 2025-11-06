import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    returned_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            returned_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        isInner = False
        split_nodes = []
        for part in parts:
            if isInner:
                split_nodes.append(TextNode(part, text_type))
                isInner = False
            else:
                if part != "":
                    split_nodes.append(TextNode(part, TextType.PLAIN))
                isInner = True
        returned_nodes.extend(split_nodes)

    return returned_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
