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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    ret_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            ret_nodes.append(node)
            continue
        inner_nodes = []
        text_rest = node.text
        for match in matches:
            image_alt, image_link = match
            sections = text_rest.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                inner_nodes.append(TextNode(sections[0], TextType.PLAIN))
            inner_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_rest = sections[1]

        if text_rest != "":
            inner_nodes.append(TextNode(text_rest, TextType.PLAIN))

        ret_nodes.extend(inner_nodes)

    return ret_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    ret_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            ret_nodes.append(node)
            continue
        inner_nodes = []
        text_rest = node.text
        for match in matches:
            link_desc, link = match
            sections = text_rest.split(f"[{link_desc}]({link})", 1)
            if sections[0] != "":
                inner_nodes.append(TextNode(sections[0], TextType.PLAIN))
            inner_nodes.append(TextNode(link_desc, TextType.LINK, link))
            text_rest = sections[1]

        if text_rest != "":
            inner_nodes.append(TextNode(text_rest, TextType.PLAIN))

        ret_nodes.extend(inner_nodes)

    return ret_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.PLAIN)
    transformed_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    transformed_nodes = split_nodes_delimiter(transformed_nodes, "_", TextType.ITALIC)
    transformed_nodes = split_nodes_delimiter(transformed_nodes, "`", TextType.CODE)
    transformed_nodes = split_nodes_image(transformed_nodes)
    transformed_nodes = split_nodes_link(transformed_nodes)

    return transformed_nodes
