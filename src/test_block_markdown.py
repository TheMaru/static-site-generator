import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


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


class TestBlockToBlockType(unittest.TestCase):
    def test_is_paragraph(self):
        block = "just a\nparagraph"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_is_headline(self):
        h1 = "# headline"
        h2 = "## headline"
        h3 = "### headline"
        h4 = "#### headline"
        h5 = "##### headline"
        h6 = "###### headline"
        h7 = "####### not a headline"
        no_h = "some text"

        self.assertEqual(BlockType.HEADING, block_to_block_type(h1))
        self.assertEqual(BlockType.HEADING, block_to_block_type(h2))
        self.assertEqual(BlockType.HEADING, block_to_block_type(h3))
        self.assertEqual(BlockType.HEADING, block_to_block_type(h4))
        self.assertEqual(BlockType.HEADING, block_to_block_type(h5))
        self.assertEqual(BlockType.HEADING, block_to_block_type(h6))
        self.assertNotEqual(BlockType.HEADING, block_to_block_type(h7))
        self.assertNotEqual(BlockType.HEADING, block_to_block_type(no_h))

    def test_is_code_block(self):
        code = "```\nsome code\n```"
        block_type = block_to_block_type(code)
        self.assertEqual(BlockType.CODE, block_type)

        no_code = "``\nsome string\n``"
        no_code2 = "```\nno code"
        block_type = block_to_block_type(no_code)
        block_type2 = block_to_block_type(no_code2)
        self.assertNotEqual(BlockType.CODE, block_type)
        self.assertNotEqual(BlockType.CODE, block_type2)

        ml_code = "```\nsome\n more \n code\n```"
        block_type = block_to_block_type(ml_code)
        self.assertEqual(BlockType.CODE, block_type)

    def test_is_quote(self):
        quote = ">this is a quote"
        quote2 = "> also quote"
        no_quote = "<no quote"
        no_quote2 = "< no quote"
        multiline_quote = "> ml\n> quote"
        not_ml_quote = "> no\n< quote"

        quote_block = block_to_block_type(quote)
        quote_block2 = block_to_block_type(quote2)
        no_quote_block = block_to_block_type(no_quote)
        no_quote_block2 = block_to_block_type(no_quote2)
        ml_quote_block = block_to_block_type(multiline_quote)
        not_ml_quote_block = block_to_block_type(not_ml_quote)

        self.assertEqual(BlockType.QUOTE, quote_block)
        self.assertEqual(BlockType.QUOTE, quote_block2)
        self.assertNotEqual(BlockType.QUOTE, no_quote_block)
        self.assertNotEqual(BlockType.QUOTE, no_quote_block2)
        self.assertEqual(BlockType.QUOTE, ml_quote_block)
        self.assertNotEqual(BlockType.QUOTE, not_ml_quote_block)

    def test_is_ul(self):
        ul = "-this is a ul"
        ul2 = "- also ul"
        no_ul = "no ul"
        multiline_ul = "- ml\n- ul"
        not_ml_ul = "- no\n ul"

        ul_block = block_to_block_type(ul)
        ul_block2 = block_to_block_type(ul2)
        no_ul_block = block_to_block_type(no_ul)
        ml_ul_block = block_to_block_type(multiline_ul)
        not_ml_ul_block = block_to_block_type(not_ml_ul)

        self.assertEqual(BlockType.UNORDERED_LIST, ul_block)
        self.assertEqual(BlockType.UNORDERED_LIST, ul_block2)
        self.assertNotEqual(BlockType.UNORDERED_LIST, no_ul_block)
        self.assertEqual(BlockType.UNORDERED_LIST, ml_ul_block)
        self.assertNotEqual(BlockType.UNORDERED_LIST, not_ml_ul_block)

    def test_is_ol(self):
        ol = "1.this is a ol"
        ol2 = "1. also ol"
        no_ol = "no ol"
        multiline_ol = "1. ml\n2. ol"
        not_ml_ol = "1. no\n3. ol"

        ol_block = block_to_block_type(ol)
        ol_block2 = block_to_block_type(ol2)
        no_ol_block = block_to_block_type(no_ol)
        ml_ol_block = block_to_block_type(multiline_ol)
        not_ml_ol_block = block_to_block_type(not_ml_ol)

        self.assertEqual(BlockType.ORDERED_LIST, ol_block)
        self.assertEqual(BlockType.ORDERED_LIST, ol_block2)
        self.assertNotEqual(BlockType.ORDERED_LIST, no_ol_block)
        self.assertEqual(BlockType.ORDERED_LIST, ml_ol_block)
        self.assertNotEqual(BlockType.ORDERED_LIST, not_ml_ol_block)
