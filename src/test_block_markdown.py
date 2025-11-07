import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_returns_single_line(self):
        string = "# This is a heading"
        blocks = markdown_to_blocks(string)

        self.assertListEqual(blocks, [string])

    def test_returns_blocks(self):
        md = """
First paragraph

Second paragraph
        """
        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, ["First paragraph", "Second paragraph"])

        md = """
 First paragraph 

  Second paragraph
        """
        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_remove_empty_lines_with_spaces(self):
        md = """
        First

        Second



        Third
        """
        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, ["First", "Second", "Third"])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
