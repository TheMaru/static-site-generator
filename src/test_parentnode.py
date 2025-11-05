import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_init(self):
        child = LeafNode("a", "just a link", {"href": "foo.bar", "target": "_blank"})
        parent = ParentNode("p", [child])

        self.assertEqual(parent.tag, "p")
        self.assertEqual(parent.value, None)
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, None)

    def test_to_html_value_error(self):
        leaf = LeafNode("span", "child")
        with self.assertRaises(ValueError) as caught:
            no_tag = ParentNode(None, [leaf])
            no_tag.to_html()
            self.assertIn("tag is missing", str(caught.exception))

        with self.assertRaises(ValueError) as caught:
            empty_tag = ParentNode("", [leaf])
            empty_tag.to_html()
            self.assertIn("tag is missing", str(caught.exception))

        with self.assertRaises(ValueError) as caught:
            none_children = ParentNode("p", None)
            none_children.to_html()
            self.assertIn("children are missing", str(caught.exception))

        with self.assertRaises(ValueError) as caught:
            no_children = ParentNode("p", [])
            no_children.to_html()
            self.assertIn("children are missing", str(caught.exception))

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div", [child_node], {"id": "special-div", "class": "my-class"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div id="special-div" class="my-class"><span>child</span></div>',
        )
