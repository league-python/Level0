import logging
import shutil
from pathlib import Path

from invoke import task
from slugify import slugify
from tasklib import *
import os
import frontmatter

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

tasks_dir = Path(__file__).parent.absolute()

def get_assignment(path):
    """Read an assignment and construct a dict of the important information"""

    path = Path(path)
    meta_path = path / '.assignment.yaml'

    if not meta_path.exists():
        return {}

    meta = yaml.safe_load(meta_path.read_text())

    meta['sources'] = []
    meta['texts'] = {}
    meta['resources'] = []

    for f in path.glob('*.py'):
        meta['sources'].append(f)

    for f in path.glob('*.md'):
        meta['texts'][f.stem] = f

    for f in list(path.glob('*.png')) + list(path.glob('*.gif')):
        meta['resources'].append(f)

    return meta

def write_assignment_text(asgn_dir, ad: dict):
    from textwrap import dedent
    from tasklib.render import render

    if not 'trinket' in ad['texts']:
        return

    file_name = ad['sources'][0].name

    text = ad['texts']['trinket'].read_text()

    return render('assignment.md',
           frontmatter={'title': ad['title']},
           title=ad['title'],
           working_directory=asgn_dir,
           content=text)

def make_sidebar():
    """Walk the directory and print out the assignment metadata"""

    def get_title_from_md(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        return post.get('title', 'No Title')

    config = get_config(tasks_dir)
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


def update_config(sidebar):

    config_file = tasks_dir / 'docs/src/.vuepress/config.yml'

    config = yaml.safe_load(config_file.read_text())

    config['themeConfig']['sidebar'] = sidebar

    config_file.write_text(yaml.dump(config))


@task
def dev(ctx, directory='.'):

    root_dir = tasks_dir

    config = get_config(tasks_dir)
    ms = Path(config['module_source'])

    lesson_root = config['lesson_root']

    for lesson, assignments in config['lessons'].items():

        l_path = lesson_root / lesson

        if not l_path.exists():
            l_path.mkdir(parents=True)

        for assign in assignments:

            meta = get_assignment(ms / assign)

            if not meta.get('title'):
                logger.info(f"Skipping {assign} because it has no title")
                continue

            asgn_path = lesson_root / lesson / slugify(meta['title'])

            if not asgn_path.exists():
                asgn_path.mkdir(parents=True)

            for f in list(meta['resources']) + list(meta['sources']):
                f = Path(f)
                print(f"Copying {f}")
                shutil.copy(f, asgn_path / f.name)

            if 'trinket' in meta['texts']:
                print(f"Writing {asgn_path}")
                text = write_assignment_text(asgn_path, meta)
                (asgn_path / 'index.md').write_text(text)

    sidebar = make_sidebar()

    update_config(sidebar)





