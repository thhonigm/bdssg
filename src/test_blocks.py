import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)

class TestMarkdown(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_no_block(self):
        text = "This is text."
        self.assertEqual(markdown_to_blocks(text), [text])

    def test_no_block_space(self):
        self.assertEqual(markdown_to_blocks("\n  This is \ntext.\n   \n"), ["This is\ntext."])

    def test_block(self):
        self.assertEqual(markdown_to_blocks("""
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
), [
    "# This is a heading",
    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
    """* This is the first list item in a list block
* This is a list item
* This is another list item""",
])

class TestBlockTypes(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading5(self):
        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_heading_too_long(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_heading_space_missing(self):
        block = "###This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_empty(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code(self):
        block = """```
#include <stdio.h>

int main(int argc, char** argv)
{
    printf("Hello, %s!\n", (argc > 0) ? argv[1] : "world");
    return 0;
}
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_empty(self):
        block = "> "
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote(self):
        block = """> 
> This is a quote.
> Third line."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote0(self):
        block = """ > 
> This is not a quote."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_quote0(self):
        block = """ > 
> This is not a quote."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_quote1(self):
        block = """> 
 > This is not a quote."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_empty(self):
        block = "* "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_empty_1(self):
        block = "- "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list(self):
        block = """* Eins
* Zwei
* Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_empty_1(self):
        block = """- Eins
- Zwei
- Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_not_unordered_list__mixed(self):
        block = """- Eins
* Zwei
* Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_unordered_list(self):
        block = """ * Eins
* Zwei
* Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_unordered_list_empty_1(self):
        block = """-Eins
- Zwei
- Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_empty(self):
        block = "1. "
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list(self):
        block = """1. Eins
2. Zwei
3. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        block = """1.Eins
2. Zwei
3. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_1(self):
        block = """1.Eins
2. Zwei
 3. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_2(self):
        block = """2. Eins
3. Zwei
4. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_3(self):
        block = """1. Eins
2 Zwei
3. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_4(self):
        block = """1. Eins
3. Zwei
4. Drei"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

