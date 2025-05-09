from textnode import TextNode, TextType
import os
import shutil
from copystatic import copy_files_recursive
from  markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

dir_path_static = "./static"
dir_path_public = "./public"

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        src_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(src_entry_path):
            os.makedirs(dest_entry_path, exist_ok=True)
            generate_pages_recursive(src_entry_path, template_path, dest_entry_path)
        
        elif entry.endswith(".md"):
            dest_entry_path = os.path.splitext(dest_entry_path)[0] + ".html"
            generate_page(src_entry_path, template_path, dest_entry_path)


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    template_path = "template.html"
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Copying complete.")
    
    generate_pages_recursive("content", template_path, "public")
    print("Page generated successfully.")


    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()