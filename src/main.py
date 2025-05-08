from textnode import TextNode, TextType
import os
import shutil

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(source_path):
            print(f"Copying directory {source_path} to {dest_path}")
            copy_static(source_path, dest_path)
        else:
            print(f"Copying file {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)

def main():
    copy_static("static", "public")
    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()