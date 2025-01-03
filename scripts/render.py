from os import walk, makedirs
from markdown import markdown
from pathlib import Path
import re
import html

def main():

    file_index: dict[str, str] = {}

    for (path, dirs, files) in walk("World"):
        path = path.replace("\\", "/")
        page_index = []
        for file in files:
            name, ending, *_ = file.split('.')
            if ending == "md":
                file_index[name] = path + "/" + file
                page_index.append(f'<li><a href="/Thousndoor/{file_index[name].replace(".md", ".html")}">🗎 {name}</a>')
        for dir in dirs:
            href = path + "/" + dir
            page_index.append(f'<li><a href="/Thousndoor/{href}">🗀 {dir}</a>')

        makedirs("docs/" + path, exist_ok=True)
        pages = "\n".join(page_index).encode('ascii', 'xmlcharrefreplace').decode()
        with open("docs/" + path + "/index.html", mode="w+") as i:
            i.write(header)
            i.write("<body>")
            i.write(make_breadcrumbs(path, False))
            i.write("<ul>")
            i.write(pages)
            i.write("</ul></body>")

    template = open("scripts/text.html.template").read()

    for file, path in file_index.items():
        with open(path) as md:
            text = md.read()

        # text = html.escape(text)
        text = markdown(text)
        text = insert_links(text, file_index)
        parent = str(Path(path).parent)
        makedirs("docs/" + parent, exist_ok=True)

        data = {
            "breadcrumbs": make_breadcrumbs(path, True),
            "title": file,
            "content": text
        }

        open("docs/" + path.replace(".md", ".html"), mode="wb").write(template.format(**data).encode('ascii', 'xmlcharrefreplace'))

header = """<head>
<link rel="stylesheet" href="/Thousndoor/style.css">
</head>
"""

link_regex = re.compile(r"\[\[([\w\s']*)\]\]|\[([\w\s']*)\]\(([\w\s']*)\)")

def insert_links(markdown: str, index: dict[str, str]) -> str: 
    links = re.finditer(link_regex, markdown)
    for link in links:
        text = link.group(1)
        target = link.group(2) or text
        if target in index:
            href = index[target].replace(".md", ".html")
            html = f'<a href="/Thousndoor/{href}">{text}</a>'
        else:
            html = f'<span class="dead-link">{text}</span>'
                
        markdown = markdown.replace(link.group(0), html)

    return markdown

def make_breadcrumbs(path, include_tail) -> str:
    print("making breadcrumbs for", path)
    *breadcrumbs, tail = path.split("/")
    breadcrumbs = [f'<a href={"/".join([".."] * (len(breadcrumbs) - i - 1) + (["."] if include_tail else [".."]))}>{n}</a>' for i, n in enumerate(breadcrumbs)]
    return '<span class="breadcrumb-sep"> &gt; </span>'.join(breadcrumbs + [tail.split('.')[0]])

if __name__ == "__main__":
    main()