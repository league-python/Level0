
from .config import  update_config
from .lesson import make_sidebar
from .assignments import get_assignment, write_assignment_text
from .render import render
from .trinket import *
import shutil
import logging
from slugify import slugify


logger = logging.getLogger(__name__)

def build_source(root_dir):

    config = get_config(root_dir)
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

    sidebar = make_sidebar(root_dir)

    update_config(root_dir, sidebar)
