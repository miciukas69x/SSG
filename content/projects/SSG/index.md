# Building My Own Static Site Generator

[< Back Home](/)

![ssg photo](/images/ssg.png)

> "From plain text and templates I forged a tool — modest in scope, but enough to build a world of pages."

[View on GitHub](https://github.com/miciukas69x/SSG)

## Introduction

This project is my own static site generator (SSG) written in Python. I created it to understand how websites can be built from plain text and templates without relying on frameworks. Every page on this site is generated with it.

## Core Features

- Converts Markdown (.md) files into HTML.
- Applies a shared template (template.html) across all pages.
- Copies assets from static/ into to the output folder.
- Generates blog posts, project pages, and a homepage.
- Simple shell scripts for building and previewing (./build.sh  ./main.sh).

## What I learned

- How Markdown parsing works (blocks, inline styles, code snippets).
- Writing file-system logic to recursively generate pages.
- Using Python modules to keep code clean and reusable.
- Why **templates** are powerful for consistent design.
- The discipline of "eat your own dogfood"

## Conclusion

This project gave me a deeper appreciation for how static site tool like Hugo or Jekyll work under the hood. It's not about just having a site - it's about knowing how to make the tool that makes the website. The SSG started as a learning exercise, but now it's the backbone of my personal site and a foundation I can keep expanding.