import unittest
from textnode import TextNode, TextType
from text_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("Plain text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiter")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_simple_bold(self):
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
        node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_multiple_nodes_input(self):
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
        node = TextNode("Text with unclosed **bold", TextType.TEXT)
        with self.assertRaises(Exception):  
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_no_match(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_image_empty_text(self):
        node = TextNode(
            "![image1](https://example.com/img1)![image2](https://example.com/img2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://example.com/img1"),
                TextNode("image2", TextType.IMAGE, "https://example.com/img2"),
            ],
            new_nodes,
        )

    def test_split_image_multiple_nodes(self):
        nodes = [
            TextNode("Text with ![img1](https://example.com/1)", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "https://example.com/existing"),
            TextNode("More text with ![img2](https://example.com/2)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://example.com/1"),
                TextNode("Already an image", TextType.IMAGE, "https://example.com/existing"),
                TextNode("More text with ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://example.com/2"),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link_no_match(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_link_empty_text(self):
        node = TextNode(
            "[link1](https://example.com/1)[link2](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("Text with [link1](https://example.com/1)", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "https://example.com/existing"),
            TextNode("More text with [link2](https://example.com/2)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("Already a link", TextType.LINK, "https://example.com/existing"),
                TextNode("More text with ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )


def test_text_to_textnodes():
    text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/img.png) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    
    assert len(nodes) == 10
    
    assert nodes[0].text == "This is "
    assert nodes[0].text_type == TextType.TEXT
    
    assert nodes[1].text == "text"
    assert nodes[1].text_type == TextType.BOLD
    
    assert nodes[2].text == " with an "
    assert nodes[2].text_type == TextType.TEXT
    
    assert nodes[3].text == "italic"
    assert nodes[3].text_type == TextType.ITALIC
    
    assert nodes[4].text == " word and a "
    assert nodes[4].text_type == TextType.TEXT
    
    assert nodes[5].text == "code block"
    assert nodes[5].text_type == TextType.CODE
    
    assert nodes[6].text == " and an "
    assert nodes[6].text_type == TextType.TEXT
    
    assert nodes[7].text == "image"
    assert nodes[7].text_type == TextType.IMAGE
    assert nodes[7].url == "https://example.com/img.png"
    
    assert nodes[8].text == " and a "
    assert nodes[8].text_type == TextType.TEXT
    
    assert nodes[9].text == "link"
    assert nodes[9].text_type == TextType.LINK
    assert nodes[9].url == "https://boot.dev"


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_with_excessive_newlines(self):
        md = """
First paragraph


Second paragraph



Third paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )