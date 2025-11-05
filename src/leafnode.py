from __future__ import annotations

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, [], props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError()
        if self.tag == "" or self.tag is None:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
