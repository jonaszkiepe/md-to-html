import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_links,
    split_nodes_images,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word", "text"),
            ]
        )

    def test_code_end(self):
        node = TextNode("this is random `code`", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("this is random ", "text"),
                TextNode("code", "code"),
            ]
        )

    def test_italic_beginning(self):
        node = TextNode("*italic* is giuseppe", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("italic", "italic"),
                TextNode(" is giuseppe", "text"),
            ]
        )

    def test_wrong_delimiter(self):
        node = TextNode("_italic is giuseppe", text_type_text)
        self.assertRaises(
            Exception,
            lambda: split_nodes_delimiter([node], "_", text_type_italic),
        )

    def test_custom_node(self):
        node = TextNode("-italic-", text_type_link)
        self.assertEqual(
            split_nodes_delimiter([node], "-", text_type_link),
            [
                TextNode("-italic-", text_type_link)
            ]
        )

    def test_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
            )
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
            ]
        )

    def test_image_two(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another one",
            text_type_text,
            )
        node2 = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another one",
            text_type_text,
            )
        new_nodes = split_nodes_images([node, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
                TextNode(" and another one", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
                TextNode(" and another one", text_type_text),
            ]
        )


    def test_link(self):
        node = TextNode(
            "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another one",
            text_type_text,
            )
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                TextNode(" and another one", text_type_text),
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ]
        )


if __name__ == "__main__":
    unittest.main()
