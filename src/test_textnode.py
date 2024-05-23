import unittest

from textnode import TextNode, text_node_to_html_node

from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_text_type_dif(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)


class TestNodeConversion(unittest.TestCase):
    def test_type_error(self):
        self.assertRaises(
            TypeError,
            text_node_to_html_node,
            TextNode(text=text_type_text, text_type="jiberish", url=None)
        )

    def test_text(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="text", url=None)),
            LeafNode(value=text_type_text, tag=None, props=None)
        )

    def test_bold(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="bold", url=None)),
            LeafNode(value=text_type_text, tag="b", props=None)
        )
        
    def test_italic(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="italic", url=None)),
            LeafNode(value=text_type_text, tag="i", props=None)
        )

    def test_code(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="code", url=None)),
            LeafNode(value=text_type_text, tag="code", props=None)
        )

    def test_link(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="link", url="https://www.google.com")),
            LeafNode(value=text_type_text, tag="a", props={"href": "https://www.google.com"})
        )

    def test_image(self):
        self.assertEqual(
            text_node_to_html_node(TextNode(text=text_type_text, text_type="image", url="https://www.google.com")),
            LeafNode(value="", tag="img", props={"src": "https://www.google.com", "alt": text_type_text})
        )

if __name__ == "__main__":
    unittest.main()

