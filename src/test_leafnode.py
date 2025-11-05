import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        link = LeafNode("a", "link text", {"href": "foo.bar", "target": "_blank"})

        self.assertEqual(link.tag, "a")
        self.assertEqual(link.value, "link text")
        self.assertEqual(link.children, [])
        self.assertEqual(link.props, {"href": "foo.bar", "target": "_blank"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        link = LeafNode("a", "link text", {"href": "foo.bar", "target": "_blank"})

        self.assertEqual(
            link.to_html(), '<a href="foo.bar" target="_blank">link text</a>'
        )
