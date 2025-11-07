import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_returns_single(self):
        text = "This is text with ![rick roll](https://i.imgur.com/aKaOqIh.gif) in it"
        image_data = extract_markdown_images(text)

        self.assertEqual(image_data, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_returns_multiple(self):
        text = "This is text with ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) in it"
        image_data = extract_markdown_images(text)

        self.assertEqual(
            image_data,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_returns_single(self):
        text = "This is text with [to foobar](http://foo.bar) in it"
        link_data = extract_markdown_links(text)

        self.assertEqual(link_data, [("to foobar", "http://foo.bar")])

    def test_returns_multiple(self):
        text = "This is text with [to foobar](http://foo.bar) and [bla fasel](http://www.blafasel.com) in it"
        link_data = extract_markdown_links(text)

        self.assertEqual(
            link_data,
            [
                ("to foobar", "http://foo.bar"),
                ("bla fasel", "http://www.blafasel.com"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
        )

    def test_no_images(self):
        node = TextNode("just some text", TextType.PLAIN)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(new_nodes, [TextNode("just some text", TextType.PLAIN)])


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://foo.bar) and another [second link](https://bla.fasel)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://foo.bar"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://bla.fasel"),
            ],
        )

    def test_no_links(self):
        node = TextNode("just some text", TextType.PLAIN)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(new_nodes, [TextNode("just some text", TextType.PLAIN)])


class TestTextToTextnodes(unittest.TestCase):
    def test_splits_correctly(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
