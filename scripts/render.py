from os import walk, makedirs
from markdown2 import markdown
from pathlib import Path
import re
import os, shutil

def main():

    file_index: dict[str, str] = {}

    build_dir("World", file_index)
    build_dir("Rules II/Public", file_index)

def build_dir(dir, file_index):
    shutil.rmtree("docs/" + dir)
    for (path, dirs, files) in walk(dir):
        path = path.replace("\\", "/")
        page_index = []
        for file in files:
            name, ending, *_ = file.split('.')
            if ending == "md" and name != "index":
                file_index[name] = path + "/" + file
                page_index.append(f'<li><a href="/Thousndoor/{file_index[name].replace(".md", ".html")}">{name}</a>')
        for dir in dirs:
            href = path + "/" + dir
            page_index.append(f'<li><a href="/Thousndoor/{href}">{dir}</a>')

        makedirs("docs/" + path, exist_ok=True)
        pages = "\n".join(sorted(page_index))
        with open("docs/" + path + "/index.html", mode="w+") as i:
            i.write(header)
            i.write("<body>")
            i.write(make_breadcrumbs(path, False))
            i.write("<ul>")
            i.write(pages)
            i.write("</ul><span id=\"placeholder\"></span></body>")

    template = open("scripts/text.html.template").read()

    for file, path in file_index.items():
        with open(path) as md:
            text = md.read()

        # text = html.escape(text)
        text = insert_links(text, file_index)
        text = markdown(text, extras=['nl2br', 'smarty-pants', 'cuddled-lists', 'tag-friendly', 'tables'])
        parent = str(Path(path).parent)
        makedirs("docs/" + parent, exist_ok=True)

        data = {
            "breadcrumbs": make_breadcrumbs(path, True),
            "title": file,
            "content": text
        }


        final = template.format(**data).encode('utf-8', 'xmlcharrefreplace').decode()
        # if Path("docs/" + path.replace(".md", ".html")).exists():
        #     final = open("docs/" + path.replace(".md", ".html")).read().replace("<span id=\"placeholder\"></span>", final)

        open("docs/" + path.replace(".md", ".html"), mode="w+").write(final)

header = """<head>
<link rel="stylesheet" href="/Thousndoor/style.css">
<meta charset="UTF-8">
</head>
"""

link_regex = re.compile(r"\[\[([\w\s']*)\]\]|\[([\w\s']*)\]\(([\w\s']*)\)")

def insert_links(markdown: str, index: dict[str, str]) -> str: 
    
    def sub(match: re.Match) -> str:
        text = match.group(1)
        target = match.group(2) or text
        if target in index:
            href = index[target].replace(".md", ".html")
            return f'<a href="/Thousndoor/{href}">{text}</a>'
        else:
            return f'<span class="dead-link">{text}</span>'

    return link_regex.sub(sub, markdown)

def make_breadcrumbs(path: str, include_tail) -> str:
    *breadcrumbs, tail = path.split("/")
    breadcrumbs = [f'<a href={"/".join([".."] * (len(breadcrumbs) - i - 1) + (["."] if include_tail else [".."]))}>{n}</a>' for i, n in enumerate(breadcrumbs)]
    return '<li class="breadcrumb-sep"> &gt; </li>'.join(breadcrumbs + [tail.split('.')[0]])

if __name__ == "__main__":
    main()