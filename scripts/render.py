from os import walk, makedirs
from markdown import markdown
from pathlib import Path

file_index: dict[str, str] = {}

for (path, dirs, files) in walk("World"):
    # print(path, dirs, files)
    for file in files:
        name, ending, *_ = file.split('.')
        if ending == "md":
            file_index[name] = path.replace("\\", "/") + "/" + file


for file, path in file_index.items():
    with open(path) as md:
        text = md.read()
    rendered = markdown(text)
    parent = str(Path(path).parent)
    makedirs("html/" + parent, exist_ok=True)
    open("html/" + path.replace(".md", ".html"), mode="w+").write(rendered)