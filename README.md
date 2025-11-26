# SSG
*A minimal static site generator in Python.*

`ssg` is a lightweight static site generator written in Python.  
It takes your content (Markdown, templates, assets), processes it, and spits out a fast, static website you can host anywhere.

---

## Features

- 📝 **Markdown to HTML**  
  Convert `.md` files into clean HTML pages.

- 🎨 **Template support**  
  Reuse layouts (headers, footers, navigation) instead of copy-pasting HTML.

- 📁 **Static assets**  
  Copy CSS, JS, and images to the output folder unchanged.

- 🧩 **Config-driven**  
  Control input/output directories and metadata from a single config file.

- ⚙️ **CLI usage**  
  Simple command-line interface: build, clean, and preview your site.

---

## Project structure

Typical layout (you can adjust if your repo differs):

```txt
ssg/
├─ ssg/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ builder.py
│  ├─ templates/
│  │  └─ base.html
│  └─ utils.py
├─ content/
│  ├─ index.md
│  └─ about.md
├─ static/
│  ├─ styles.css
│  └─ script.js
├─ output/          # generated site (ignored by git)
├─ ssg.config.yaml  # or .toml / .json depending on your setup
├─ pyproject.toml   # or requirements.txt / setup.cfg
└─ README.md
