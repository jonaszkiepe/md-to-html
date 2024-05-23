import unittest

from block_markdown import (
    block_to_html_code,
    block_to_html_heading,
    block_to_html_ordered_list,
    block_to_html_paragraph,
    block_to_html_quote,
    block_to_html_unordered_list,
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_code,
    block_type_heading,
    block_type_quote,
    markdown_to_html_node,
)
from htmlnode import LeafNode, ParentNode

class TestMarkdownToBlock(unittest.TestCase):
    def test_split_blocks(self):
        markdown = ("""
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items 
 """)
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\n"
                "This is the same paragraph on a new line",
                "* This is a list\n"
                "* with items",
            ]
        )

    def test_block_to_block_type_paragraph(self):
        md_block = "What is up"
        self.assertEqual(
            block_to_block_type(md_block),
            block_type_paragraph
        )

    def test_block_to_block_type_code(self):
        md_block = ( 
                   "``` print('Hello World')"
                   "just kidding"
                   "some code.."
                   "```"
                   )
        self.assertEqual(
                block_to_block_type(md_block),
                block_type_code
                )

    def test_block_to_block_type_quote(self):
        md_block = ( 
                   ">Hey"
                   ">This is quote"
                   "> RIGHT"
                   ">> YES!"
                   )
        self.assertEqual(
                block_to_block_type(md_block),
                block_type_quote
                )

    def test_block_to_block_type_unordered_list(self):
        md_block = ( 
                   "- hey\n"
                   "- this is a list\n"
                   "* this is also a list"
                   "- welcome to narnia"
                   )
        self.assertEqual(
                block_to_block_type(md_block),
                block_type_unordered_list
                )

    def test_block_to_block_type_ordered_list(self):
        md_block = ( 
                   "1. hey\n"
                   "2. this is a list\n"
                   "3. this is also a list\n"
                   "4. welcome to narnia"
                   )
        self.assertEqual(
                block_to_block_type(md_block),
                block_type_ordered_list
                )

    def test_block_to_block_type_heading(self):
        md_block = ( 
                    "# HELLO THIS IS HEADING"
                   )
        self.assertEqual(
                block_to_block_type(md_block),
                block_type_heading
                )


class TestBlockToHtml(unittest.TestCase):
    def test_paragraph(self):
        block = "hey this is not fun\njust kidding"
        self.assertEqual(
            block_to_html_paragraph(block),
            ParentNode(
                [
                    LeafNode("hey this is not fun"),
                    LeafNode("just kidding"),
                ],
                "p"
            )
        )


    def test_heading(self):
        block = "### hey this is not fun\njust kidding"
        self.assertEqual(
            block_to_html_heading(block),
            ParentNode( [
                    LeafNode("hey this is not fun\njust kidding"),
                ],
                "h3"
            )
        )


    def test_code(self):
        block = "```hey this is not fun\njust kidding```"
        self.assertEqual(
            block_to_html_code(block),
            ParentNode(
                [
                    LeafNode("hey this is not fun\njust kidding", "pre")
                ],
                "code"
            )
        )


    def test_quote(self):
        block = ">hey this is not fun\n>just kidding\n>lol"
        self.assertEqual(
            block_to_html_quote(block),
            ParentNode(
                [
                    LeafNode("hey this is not fun"),
                    LeafNode("just kidding"),
                    LeafNode("lol")
                ],
                "quoteblock"
            )
        )


    def test_unordered_list(self):
        block = "* hey this is not fun\n- just kidding\n* lol"
        self.assertEqual(
            block_to_html_unordered_list(block),
            ParentNode(
                [
                    LeafNode("hey this is not fun", "li"),
                    LeafNode("just kidding", "li"),
                    LeafNode("lol", "li")
                ],
                "ul"
            )
        )


    def test_ordered_list(self):
        block = "1. hey this is not fun\n2. just kidding\n3. lol"
        self.assertEqual(
            block_to_html_ordered_list(block),
            ParentNode(
                [
                    LeafNode("hey this is not fun", "li"),
                    LeafNode("just kidding", "li"),
                    LeafNode("lol", "li")
                ],
                "ol"
            )
        )


class MdToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = ("""
hey this is not fun\njust kidding

### hey this is not fun\njust kidding

```hey this is not fun\njust kidding```

>hey this is not fun\n>just kidding\n>lol

* hey this is not fun\n- just kidding\n* lol

1. hey this is not fun\n2. just kidding\n3. lol
 """)
        self.assertEqual(
            markdown_to_html_node(markdown),
            ParentNode(
                [
                    ParentNode(
                        [
                            LeafNode("hey this is not fun"),
                            LeafNode("just kidding"),
                        ],
                        "p"
                    ),
                    ParentNode( 
                        [
                            LeafNode("hey this is not fun\njust kidding"),
                        ],
                        "h3"
                    ),
                    ParentNode(
                        [
                            LeafNode("hey this is not fun\njust kidding", "pre")
                        ],
                        "code"
                    ),
                    ParentNode(
                        [
                            LeafNode("hey this is not fun"),
                            LeafNode("just kidding"),
                            LeafNode("lol")
                        ],
                        "quoteblock"
                    ),
                    ParentNode(
                        [
                            LeafNode("hey this is not fun", "li"),
                            LeafNode("just kidding", "li"),
                            LeafNode("lol", "li")
                        ],
                        "ul"
                    ),
                    ParentNode(
                        [
                            LeafNode("hey this is not fun", "li"),
                            LeafNode("just kidding", "li"),
                            LeafNode("lol", "li")
                        ],
                        "ol"
                    )
                ],
                "div"
            )
        )


if __name__ == "__main__":
    unittest.main()

