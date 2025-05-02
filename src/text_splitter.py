from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text

        if delimiter not in text:
            result.append(old_node)
            continue
        
        parts = []
        remaining_text = text

        while delimiter in remaining_text:
            split_text = remaining_text.split(delimiter, 1)
            before_delimiter = split_text[0]

            if before_delimiter:
                parts.append((before_delimiter, TextType.TEXT))

            if delimiter not in split_text[1]:
                raise ValueError(f"Missing closing delimiter: {delimiter}")

            after_opening = split_text[1].split(delimiter, 1)
            delimiter_content = after_opening[0]

            if delimiter_content:
                parts.append((delimiter_content, text_type))

            remaining_text = after_opening[1]

        if remaining_text:
            parts.append((remaining_text, TextType.TEXT))

        for text_part, node_type in parts:
            result.append(TextNode(text_part, node_type))

    return result

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            result.append(old_node)
            continue
        
        remaining_text = text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            
            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            result.append(old_node)
            continue
        
        remaining_text = text
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            
            result.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result
    

def text_to_textnodes(text):
    print("running test_to_textnodes")
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes