import unittest
from textnode import TextNode, TextType
from text_splitter import split_nodes_delimiter  # adjust import to your file structure

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        # Test when delimiter isn't present
        node = TextNode("Plain text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiter")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_simple_bold(self):
        # Test simple bold case
        node = TextNode("Text with **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_code_block(self):
        # Test code block
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        # Test text with multiple delimiter pairs
        node = TextNode("Text with _italic_ and another _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " and another ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " word")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_non_text_node(self):
        # Test that non-TEXT nodes are preserved
        node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_multiple_nodes_input(self):
        # Test with multiple nodes as input
        nodes = [
            TextNode("First **bold**", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More **bold** text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "Already bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "More ")
        self.assertEqual(result[3].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, "bold")
        self.assertEqual(result[4].text_type, TextType.BOLD)
        self.assertEqual(result[5].text, " text")
        self.assertEqual(result[5].text_type, TextType.TEXT)

    def test_missing_closing_delimiter(self):
        # Test that an error is raised when closing delimiter is missing
        node = TextNode("Text with unclosed **bold", TextType.TEXT)
        with self.assertRaises(Exception):  # You can use specific exception if defined
            split_nodes_delimiter([node], "**", TextType.BOLD)