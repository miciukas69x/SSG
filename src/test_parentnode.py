import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_tag_none_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "test")]).to_html()
            
    def test_empty_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()
            
    def test_with_props(self):
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>test</span></div>')
        
    def test_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_nested_parent_nodes(self):
        inner_parent = ParentNode("div", [LeafNode("span", "inner text")])
        middle_parent = ParentNode("section", [inner_parent, LeafNode("p", "paragraph")])
        outer_parent = ParentNode("main", [middle_parent])
        self.assertEqual(
            outer_parent.to_html(),
            "<main><section><div><span>inner text</span></div><p>paragraph</p></section></main>"
        )

    def test_with_complex_props(self):
        node = ParentNode(
            "div", 
            [LeafNode("p", "text")], 
            {"id": "main", "class": "container", "data-test": "value"}
        )
        self.assertEqual(
            node.to_html(),
            '<div id="main" class="container" data-test="value"><p>text</p></div>'
        )