from __future__ import annotations


class HTMLNode:
    def __init__(
        self, tag: str, value: str, children: list[HTMLNode], props: dict[str, str]
    ) -> None:
        self.tag = tag
        self.value = value
        self.children: list[HTMLNode] = children
        self.props: dict[str, str] = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        ret_str = ""
        if self.props is None:
            return ret_str
        for key, value in self.props.items():
            ret_str += f" {key}={value}"

        return ret_str

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
