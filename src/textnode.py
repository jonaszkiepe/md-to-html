from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        return (
            self.text == other_node.text and
            self.text_type == other_node.text_type and 
            self.url == other_node.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_nodes_to_html_nodes(nodes):
    leaf_nodes = []
    for n in nodes:
        tag, props, value = None, None, n.text
        if n.text_type == text_type_text: pass
        elif n.text_type == text_type_bold: tag = "b"
        elif n.text_type == text_type_italic: tag = "i"
        elif n.text_type == text_type_code: tag = "code"
        elif n.text_type == text_type_link: tag, props = "a", {"href": n.url}
        elif n.text_type == text_type_image:
            value, tag, props = "", "img", {"src": n.url, "alt": n.text}
        else: raise TypeError("Incorrect text type")
        leaf_nodes.append(LeafNode(value=value, tag=tag, props=props))
    return leaf_nodes

