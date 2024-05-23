import unittest

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

from htmlnode import HTMLnode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLnode(
            tag="h1",
            value="yo this is a cool header",
            props={"href": "https://www.google.com"},
        )
        self.assertEqual(
            node.props_to_html(),
            " href=https://www.google.com"
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            tag="h1",
            value="Wow this works!",
            props={"href": "https://www.google.com"},
        )
        self.assertEqual(
            node.to_html(),
            "<h1 href=https://www.google.com>Wow this works!</h1>"
        )

    def test_no_value(self):
        self.assertRaises(
            ValueError,
            lambda: LeafNode(tag="h1", value=None, props={"href": "https://www.google.com"})
        )

    def test_no_tag(self):
        node = LeafNode(
            value="Wow this works!",
            props={"href": "https://www.google.com"},
        )
        self.assertEqual(
            node.to_html(),
            "Wow this works!"
        )


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        self.assertRaises(
            ValueError,
            lambda: ParentNode(
                children=[
                    LeafNode(tag="b", value="What is up!!", props={"href": "https://www.google.com"}),
                    LeafNode(tag="h1", value="What a nice day is it not?"),
                    LeafNode(tag="p", value="This is the end..", props={"href": "https://www.google.com"}),
                ],
                props={"color": "rainbow"}
            )
        )

    def test_eq(self):
        node = ParentNode(
            children=[
                LeafNode(tag="b", value="What is up!!", props={"href": "https://www.google.com"}),
                LeafNode(tag="h1", value="What a nice day is it not?"),
                LeafNode(tag="p", value="This is the end..", props={"href": "https://www.google.com"}),
            ],
            tag="div",
            props={"color": "rainbow"},
        )
        self.assertEqual(
            node.to_html(),
            "<div><b href=https://www.google.com>What is up!!</b><h1>What a nice day is it not?</h1><p href=https://www.google.com>This is the end..</p></div>"
            )

    def test_nesting(self):
        node = ParentNode(
            children=[
                LeafNode(tag="b", value="What is up!!", props={"href": "https://www.google.com"}),
                LeafNode(tag="h1", value="What a nice day is it not?"),
                LeafNode(tag="p", value="This is the end..", props={"href": "https://www.google.com"}),
                ParentNode(
                    children=[
                        LeafNode(tag="b", value="What is up!!", props={"href": "https://www.google.com"}),
                        LeafNode(tag="h1", value="What a nice day is it not?"),
                        LeafNode(tag="p", value="This is the end..", props={"href": "https://www.google.com"}),
                        ParentNode(
                            children=[
                                LeafNode(tag="b", value="What is up!!", props={"href": "https://www.google.com"}),
                                LeafNode(tag="h1", value="What a nice day is it not?"),
                                LeafNode(tag="p", value="This is the end..", props={"href": "https://www.google.com"}),
                            ],
                            tag="div",
                            props={"color": "rainbow"},
                        ),
                    ],
                    tag="div",
                    props={"color": "rainbow"},
                ),
            ],
            tag="div",
            props={"color": "rainbow"},
        )
        self.assertEqual(
            node.to_html(),
            "<div><b href=https://www.google.com>What is up!!</b><h1>What a nice day is it not?</h1><p href=https://www.google.com>This is the end..</p><div><b href=https://www.google.com>What is up!!</b><h1>What a nice day is it not?</h1><p href=https://www.google.com>This is the end..</p><div><b href=https://www.google.com>What is up!!</b><h1>What a nice day is it not?</h1><p href=https://www.google.com>This is the end..</p></div></div></div>"
            )


if __name__ == "__main__":
    unittest.main()
