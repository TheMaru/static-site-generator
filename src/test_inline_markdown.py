import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_delim_text_only(self):
        node = TextNode("this is just plain text", TextType.PLAIN)
        returned_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            returned_nodes, [TextNode("this is just plain text", TextType.PLAIN)]
        )

    def test_delim_code(self):
        node = TextNode(
            "this is just plain text, with a `code segment` in between", TextType.PLAIN
        )
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            split_nodes,
            [
                TextNode("this is just plain text, with a ", TextType.PLAIN),
                TextNode("code segment", TextType.CODE),
                TextNode(" in between", TextType.PLAIN),
            ],
        )

    def test_delim_start(self):
        node = TextNode("`code` some plain after", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            split_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" some plain after", TextType.PLAIN),
            ],
        )

    def test_delim_multiple(self):
        node = TextNode("some _italic_ words _more_ mixed", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            split_nodes,
            [
                TextNode("some ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" words ", TextType.PLAIN),
                TextNode("more", TextType.ITALIC),
                TextNode(" mixed", TextType.PLAIN),
            ],
        )

    def test_delim_multiple_nodes(self):
        node1 = TextNode("some **bold**", TextType.PLAIN)
        node2 = TextNode("more **fat** text", TextType.PLAIN)
        split_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)

        self.assertEqual(
            split_nodes,
            [
                TextNode("some ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode("more ", TextType.PLAIN),
                TextNode("fat", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_delim_non_text_node(self):
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode("more **fat** text", TextType.PLAIN)

        split_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)

        self.assertEqual(
            split_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("more ", TextType.PLAIN),
                TextNode("fat", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
        )


def test_delim_bold_and_italic(self):
    node = TextNode("**bold** and _italic_", TextType.PLAIN)
    split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)

    self.assertListEqual(
        split_nodes,
        [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ],
    )
