from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object, /) -> bool:
        if value is self:
            return True
        if not isinstance(value, TextNode):
            return NotImplemented
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    if not isinstance(text_node.text_type, TextType):
        raise TypeError(
            f"text_node.text_type must be TextType, got {type(text_node.text_type).__name__!r}"
        )

    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            assert text_node.url is not None
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            assert text_node.url is not None
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("The enum for this type does not seem to be implemented")
