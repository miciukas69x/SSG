from textnode import TextNode, TextType

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
    