import unittest
from textnode import TextNode, TextType
from text_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link

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
