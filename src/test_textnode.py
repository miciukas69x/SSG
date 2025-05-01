import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_property(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertNotEqual(node1, node2)

        node3 = TextNode("Link text", TextType.LINK, "https://example.com")
        node4 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node3, node4)

        node5 = TextNode("Link text", TextType.LINK, "https://example.com")
        node6 = TextNode("Link text", TextType.LINK, "https://different.com")
        self.assertNotEqual(node5, node6)

    def test_different_properties(self):
        node1 = TextNode("First text", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

        node3 = TextNode("Same text", TextType.BOLD)
        node4 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node3, node4)   


    def test_text(self):
        # This is the example test provided in the assignment
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
    
    def test_link(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "image.jpg")
        self.assertEqual(html_node.props["alt"], "Alt text")


if __name__ == "__main__":
    unittest.main()