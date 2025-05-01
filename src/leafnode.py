from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
    
    # Otherwise, render as an HTML tag
        props_html = self.props_to_html()
        result = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        return result