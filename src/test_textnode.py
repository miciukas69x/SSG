import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()