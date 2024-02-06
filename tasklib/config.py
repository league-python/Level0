""" Reading configuration files
"""

import os
from pathlib import Path

import yaml
import frontmatter

def update_config(root_dir, sidebar):

    config_file = root_dir / 'docs/src/.vuepress/config.yml'

    config = yaml.safe_load(config_file.read_text())

    config['themeConfig']['sidebar'] = sidebar

    config_file.write_text(yaml.dump(config))


def get_config(root='.'):
    """Read configuration from the _config.yaml file"""

    wd = Path(root)

    with open(Path.cwd().joinpath('lesson-plan.yaml')) as file:
        config = yaml.safe_load(file)

    config['module_source'] = os.environ.get('MODULE_SOURCE', None)
    config['lesson_root'] = wd / 'docs/src/lessons'

    return config

def make_sidebar(root_dir):
    """Walk the directory and print out the assignment metadata to make
    the data for the sidebar"""

    def get_title_from_md(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        return post.get('title', 'No Title')

    config = get_config(root_dir)
    ms = Path(config['module_source'])

    lesson_root = config['lesson_root']

    sidebar = [{"title": "Introduction",  "path": "/lessons" }]

    for f in lesson_root.glob('*'):
        if f.is_file():
            continue

        d = {"title": f.name, "collapsable": False, "children": []}
        for c in f.glob('*'):
            if c.is_file():
                continue
            title = get_title_from_md(c.joinpath('index.md'))
            d['children'].append({"title": title, "path": f"/lessons/{f.name}/{c.name}/"})

        sidebar.append(d)

    return sidebar
