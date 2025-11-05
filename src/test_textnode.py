import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_init(self):
        node = TextNode("text", TextType.PLAIN, "some.url")
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.PLAIN)
        self.assertEqual(node.url, "some.url")

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_equal = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node_equal)

        node_unequal = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node_unequal)

        node_italic = TextNode("italic text", TextType.ITALIC)
        node_not_italic = TextNode("italic text", TextType.PLAIN)
        self.assertNotEqual(node_italic, node_not_italic)

        node_url = TextNode("link text", TextType.LINK, "http://foo.bar")
        node_url_equal = TextNode("link text", TextType.LINK, "http://foo.bar")
        node_url_other_url = TextNode("link text", TextType.LINK, "http://blah.fasel")
        self.assertEqual(node_url, node_url_equal)
        self.assertNotEqual(node_url, node_url_other_url)

        node_url_no_link = TextNode("link text", TextType.LINK)
        self.assertNotEqual(node_url, node_url_no_link)

    def test_repr(self):
        node = TextNode("text", TextType.PLAIN, "some.url")
        r = repr(node)
        self.assertIn("TextNode(", r)
        self.assertIn(TextType.PLAIN.value, r)
        self.assertIn("some.url", r)

    class TestTextNodeToHTMLNode(unittest.TestCase):
        def test_text(self):
            node = TextNode("This is a text node", TextType.PLAIN)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, "This is a text node")

        def test_bold(self):
            node = TextNode("This is a bold node", TextType.BOLD)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is a bold node")

        def test_italic(self):
            node = TextNode("This is a italic node", TextType.ITALIC)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "i")
            self.assertEqual(html_node.value, "This is a italic node")

        def test_code(self):
            node = TextNode("This is a code node", TextType.CODE)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "code")
            self.assertEqual(html_node.value, "This is a code node")

        def test_link(self):
            node = TextNode("This is a link node", TextType.LINK, "foo.bar")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "a")
            self.assertEqual(html_node.value, "This is a link node")
            self.assertEqual(html_node.props, {"href": node.url})

        def test_image(self):
            node = TextNode("This is a image node", TextType.IMAGE, "bla.fasel")
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "img")
            self.assertEqual(html_node.value, "")
            self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})


if __name__ == "__main__":
    unittest.main()
