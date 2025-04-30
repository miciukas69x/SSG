import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
        
        # Test with empty props dictionary
        node = HTMLNode("p", "Hello, world!", None, {})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    
    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        props = {
            "href": "https://example.com",
            "target": "_blank",
            "class": "link-button"
        }
        node = HTMLNode("a", "Click me", None, props)
        
        # Since dictionaries don't guarantee order, we need to check that all props are present
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertIn(' class="link-button"', result)
        
        # Check the total length to ensure there are no extra spaces
        self.assertEqual(result.count(' '), len(props))
if __name__ == "__main__":
    unittest.main()