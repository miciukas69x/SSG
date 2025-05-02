import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    # This is the test example provided in the lesson
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    # Additional tests for images
    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "Here are multiple images: ![first](https://example.com/first.jpg) and ![second](https://example.com/second.png)"
        )
        self.assertListEqual([
            ("first", "https://example.com/first.jpg"),
            ("second", "https://example.com/second.png")
        ], matches)
    
    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images("This text has no images.")
        self.assertListEqual([], matches)
    
    # Tests for links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "Multiple links: [first](https://first.com) and [second](https://second.org)"
        )
        self.assertListEqual([
            ("first", "https://first.com"),
            ("second", "https://second.org")
        ], matches)