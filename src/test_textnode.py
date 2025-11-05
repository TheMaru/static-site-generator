import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
