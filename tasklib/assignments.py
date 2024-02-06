from pathlib import Path
import yaml
from slugify import slugify

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
