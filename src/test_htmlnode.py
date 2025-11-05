import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        headline = HTMLNode("h1", "my headline", [], {})
        link = HTMLNode("a", "link", [], {"href": "foo.bar", "target": "_blank"})
        paragraph = HTMLNode("p", "", [headline, link], {})

        self.assertEqual(headline.tag, "h1")
        self.assertEqual(headline.value, "my headline")
        self.assertEqual(headline.children, [])
        self.assertEqual(headline.props, {})

        self.assertEqual(link.tag, "a")
        self.assertEqual(link.value, "link")
        self.assertEqual(link.children, [])
        self.assertEqual(link.props, {"href": "foo.bar", "target": "_blank"})

        self.assertEqual(paragraph.tag, "p")
        self.assertEqual(paragraph.value, "")
        self.assertIn(headline, paragraph.children)
        self.assertIn(link, paragraph.children)
        self.assertEqual(paragraph.props, {})

    def test_repr(self):
        headline = HTMLNode("h1", "my headline", [], {})
        link = HTMLNode("a", "link", [], {"href": "foo.bar", "target": "_blank"})
        paragraph = HTMLNode("p", "", [headline, link], {})

        r = repr(headline)
        self.assertIn("HTMLNode(", r)
        self.assertIn("h1", r)
        self.assertIn("my headline", r)

        r = repr(link)
        self.assertIn("HTMLNode(", r)
        self.assertIn("a,", r)
        self.assertIn("link", r)
        self.assertIn("href", r)
        self.assertIn("foo.bar", r)
        self.assertIn("target", r)
        self.assertIn("_blank", r)

        r = repr(paragraph)
        self.assertIn("p,", r)
        self.assertIn("_blank", r)
        self.assertIn("my headline", r)

    def test_props_to_html(self):
        props = {"href": "foo.bar", "target": "_blank"}
        link = HTMLNode("a", "link", [], props)

        self.assertEqual(link.props_to_html(), ' href="foo.bar" target="_blank"')


if __name__ == "__main__":
    unittest.main()
