class HTMLnode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
                return "".join([f" {item}={value}" for item, value in self.props.items()])
        return ""

    def __eq__(self, other_node):
        return (
            self.tag == other_node.tag and
            self.value == other_node.value and 
            self.children == other_node.children and
            self.props == other_node.props
        )


    def __repr__(self) -> str:
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"


class LeafNode(HTMLnode):
    def __init__(self, value, tag=None, props=None):
        if value == None: raise ValueError("No Value Provided")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == None: return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLnode):
    def __init__(self, children, tag=None , props=None):
        if tag == None: raise ValueError("No tag provided")
        if children == None: raise ValueError("No children provided")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        return "<div>" + "".join(map(lambda c: c.to_html(), self.children)) + "</div>"

