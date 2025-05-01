from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one child")

        html = f"<{self.tag}"
        if self.props is not None:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        html += ">"
        
        for child in self.children:
            html += child.to_html()
    
        html += f"</{self.tag}>"
    
        return html