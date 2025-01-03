from os import walk, makedirs
from markdown import markdown
from pathlib import Path
import re
import html

def main():

    file_index: dict[str, str] = {}

    for (path, dirs, files) in walk("World"):
        page_index = []
        for file in files:
            name, ending, *_ = file.split('.')
            if ending == "md":
                file_index[name] = path.replace("\\", "/") + "/" + file
                page_index.append(f'<li><a href="/Thousndoor/{file_index[name].replace(".md", ".html")}">{name}</a>')
        for dir in dirs:
            href = path.replace("\\", "/") + "/" + dir + "/index.html"
            page_index.append(f'<li><a href="/Thousndoor/{href}">{dir}</a>')

        makedirs("docs/" + path, exist_ok=True)
        with open("docs/" + path + "/index.html", mode="w+") as i:
            i.write(header)
            i.write("<body><ul>")
            i.write("\n".join(page_index))
            i.write("</ul></body>")


    template = open("scripts/text.html.template").read()


    for file, path in file_index.items():
        with open(path) as md:
            text = md.read()

        text = html.escape(text)
        text = insert_links(text, file_index)
        rendered = markdown(text)
        parent = str(Path(path).parent)
        makedirs("docs/" + parent, exist_ok=True)

        breadcrumbs = path.split("/")[:-1]
        print(breadcrumbs)
        breadcrumbs = [f'<a href={"/".join([".."] * (len(breadcrumbs) - i - 1) + ["."])}>{n}</a>' for i, n in enumerate(breadcrumbs)]
        print(breadcrumbs)
        breadcrumbs = '<span class="breadcrumb-sep"> &gt; </span>'.join(breadcrumbs)

        data = {
            "breadcrumbs": breadcrumbs,
            "title": file,
            "content": rendered
        }

        open("docs/" + path.replace(".md", ".html"), mode="w+").write(template.format(**data))

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
        
        print(link.group(0), "->", html)
        
        markdown = markdown.replace(link.group(0), html)

    return markdown

if __name__ == "__main__":
    main()