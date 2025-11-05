from __future__ import annotations

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == "" or self.tag is None:
            raise ValueError("tag is missing")
        if self.children is None or len(self.children) == 0:
            raise ValueError("children are missing")

        children_str = ""
        for child in self.children:
            children_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
