import os
import re
from pathlib import Path
from datetime import datetime
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Check if we're in the blogs directory
    dir_name = os.path.basename(os.path.normpath(dir_path_content))
    if dir_name == "blogs":
        # Generate blog listing page (this will overwrite any index.md)
        generate_blog_listing(dir_path_content, template_path, dest_dir_path, basepath)
    
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            # Skip index.md in blogs directory since we generate the listing automatically
            if dir_name == "blogs" and filename == "index.md":
                continue
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def parse_frontmatter(markdown_content):
    """Parse YAML frontmatter from markdown content.
    Returns (metadata_dict, markdown_without_frontmatter)"""
    metadata = {}
    
    # Check for frontmatter (starts with ---)
    if not markdown_content.strip().startswith("---"):
        return metadata, markdown_content
    
    lines = markdown_content.split("\n")
    if len(lines) < 2 or lines[0].strip() != "---":
        return metadata, markdown_content
    
    # Find the closing ---
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    
    if end_idx == -1:
        return metadata, markdown_content
    
    # Parse frontmatter lines
    for i in range(1, end_idx):
        line = lines[i].strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            metadata[key] = value
    
    # Return markdown without frontmatter
    markdown_without_frontmatter = "\n".join(lines[end_idx + 1:])
    return metadata, markdown_without_frontmatter


def extract_title(md, metadata=None):
    """Extract title from metadata or markdown."""
    if metadata and "title" in metadata:
        return metadata["title"]
    
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    # Fallback: use directory name or "Untitled"
    return "Untitled"


def extract_excerpt(md, max_length=200):
    """Extract excerpt from markdown content."""
    # Remove frontmatter if present
    _, content = parse_frontmatter(md)
    
    # Remove headers and get first paragraph
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!") and not line.startswith("["):
            # Clean up markdown formatting
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # Remove links, keep text
            text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)  # Remove bold
            text = re.sub(r'\*([^\*]+)\*', r'\1', text)  # Remove italic
            if len(text) > 20:  # Only use substantial lines
                if len(text) > max_length:
                    return text[:max_length] + "..."
                return text
    return ""


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    # Parse frontmatter
    metadata, markdown_without_frontmatter = parse_frontmatter(markdown_content)
    
    # Use markdown without frontmatter for HTML generation
    node = markdown_to_html_node(markdown_without_frontmatter)
    html = node.to_html()

    title = extract_title(markdown_content, metadata)
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()


def generate_blog_listing(blogs_dir_path, template_path, dest_dir_path, basepath):
    """Generate a blog listing page from all blog posts."""
    print(f" * Generating blog listing from {blogs_dir_path}")
    
    blog_posts = []
    
    # Scan all blog subdirectories
    for item in os.listdir(blogs_dir_path):
        item_path = os.path.join(blogs_dir_path, item)
        if os.path.isdir(item_path) and item != "__pycache__":
            # Look for index.md in the subdirectory
            index_md = os.path.join(item_path, "index.md")
            if os.path.isfile(index_md):
                with open(index_md, "r") as f:
                    content = f.read()
                
                try:
                    metadata, _ = parse_frontmatter(content)
                    title = extract_title(content, metadata)
                    if title == "Untitled":
                        # Use directory name as fallback
                        title = item.replace("_", " ").replace("-", " ").title()
                    
                    # Get date from metadata or use file modification time
                    date_str = metadata.get("date", "")
                    if not date_str:
                        # Try to parse from directory name (e.g., blog001)
                        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', item)
                        if m:
                            date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
                        else:
                            # Use file modification time
                            mtime = os.path.getmtime(index_md)
                            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                    
                    excerpt = metadata.get("excerpt", "")
                    if not excerpt:
                        excerpt = extract_excerpt(content)
                    if not excerpt:
                        excerpt = "No excerpt available."
                    
                    # Determine URL path
                    blog_url = f"{basepath}blogs/{item}/"
                    
                    blog_posts.append({
                        "title": title,
                        "date": date_str,
                        "excerpt": excerpt,
                        "url": blog_url,
                        "slug": item
                    })
                except Exception as e:
                    print(f"Warning: Error processing blog {item}: {e}")
                    continue
    
    # Sort by date (newest first)
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return datetime.min
    
    blog_posts.sort(key=lambda x: parse_date(x["date"]), reverse=True)
    
    # Generate HTML for blog listing
    listing_html = '<div class="blog-listing"><h1>Blog</h1>\n'
    
    if not blog_posts:
        listing_html += '<p>No blog posts yet. Check back soon!</p>\n'
    else:
        for post in blog_posts:
            listing_html += f'''<div class="blog-post-item">
  <h2><a href="{post["url"]}">{post["title"]}</a></h2>
  <div class="blog-post-meta">{post["date"]}</div>
  <p class="blog-post-excerpt">{post["excerpt"]}</p>
</div>
'''
    
    listing_html += '</div>'
    
    # Generate the page using template
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()
    
    template = template.replace("{{ Title }}", "Blog")
    template = template.replace("{{ Content }}", listing_html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    
    # Write to blogs/index.html
    listing_dest = os.path.join(dest_dir_path, "index.html")
    dest_dir_path_parent = os.path.dirname(listing_dest)
    if dest_dir_path_parent != "":
        os.makedirs(dest_dir_path_parent, exist_ok=True)
    
    to_file = open(listing_dest, "w")
    to_file.write(template)
    to_file.close()
    
    print(f" * Generated blog listing with {len(blog_posts)} posts")
