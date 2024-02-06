""" Object structure for the lesson plan, the lessons and assignments.
Iterates through the lesson plan and writes the lessons and assignments to the
file system.
"""
import logging
import shutil
from pathlib import Path

import frontmatter
import yaml
from slugify import slugify

logger = logging.getLogger(__name__)


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


class Assignment:
    def __init__(self, lesson: "Lesson", assignment_dir):
        self.lesson = lesson
        self.ass_dir = Path(assignment_dir)

        if not self.ass_dir.exists():
            raise FileNotFoundError(f'Assignment directory nonexistant: ', assignment_dir)

        self.ass_data = get_assignment(self.ass_dir)

    @property
    def title(self):
        try:
            return self.ass_data['title']
        except KeyError:
            print('ERROR', self.ass_data)
            return ''

    @property
    def dir_name(self):
        return slugify(self.title)

    def write_dir(self, root: Path):
        from tasklib.render import render

        lesson_dir = root / self.lesson.dir_name
        ass_dir = lesson_dir / self.dir_name

        if not ass_dir.exists():
            ass_dir.mkdir(parents=True)

        ad = self.ass_data

        if not 'trinket' in ad['texts']:
            return

        # Copy the source files
        for source in ad['sources']:
            shutil.copy(source, ass_dir)

        text = ad['texts']['trinket'].read_text()

        md = render('assignment.md',
                    frontmatter={'title': ad['title']},
                    title=ad['title'],
                    working_directory=ass_dir,
                    content=text)

        (ass_dir / 'index.md').write_text(md)

        # Copy outher resources
        for f in list(ad['resources']) + list(ad['sources']):
            f = Path(f)
            shutil.copy(f, ass_dir / f.name)

        return ass_dir

    @property
    def sidebar_entry(self):

        return {
            'path': f'/lessons/{self.lesson.dir_name}/{self.dir_name}/',
            'title': self.title
        }

    def __str__(self):
        return self.title


class Lesson:

    def __init__(self, lesson_plan: "LessonPlan", lesson_data):
        self.lesson_plan = lesson_plan
        self.ld = lesson_data
        self.src_dir = self.lesson_plan.less_plan_dir

    @property
    def lesson_text(self):
        return (self.src_dir / self.ld['text']).read_text()

    @property
    def title(self):
        fm = frontmatter.loads(self.lesson_text)

        try:
            return fm['title']
        except KeyError:
            raise KeyError(f'Frontmatter for {self.ld["text"]} does not have a title')

    @property
    def dir_name(self):
        return slugify(self.title)

    def write_dir(self, root: Path):
        """Write the lesson to the root directory

        Args:
            root (Path): The root directory to write the lesson to
        """

        lesson_dir = root / self.dir_name
        lesson_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy(self.src_dir / self.ld['text'], lesson_dir / 'index.md')

        for res in self.ld['resources']:
            logger.debug(f'    Copying {res} to {lesson_dir}')
            shutil.copy(self.src_dir / 'assets' / res, lesson_dir / res)

        for ass in self.assignments:
            logger.debug(f'    Writing {ass}')
            ass.write_dir(root)

        return lesson_dir

    @property
    def sidebar_entry(self):
        """
        - collapsable: false
          title: lesson2
          children:
            - path: /lessons/lesson2/flaming-ninja-star/
              title: Flaming Ninja Star
            - path: /lessons/lesson2/turtle-spiral/
              title: Turtle Spiral

        """

        return {
            'collapsable': False,
            'title': self.title,
            'path': f'/lessons/{self.dir_name}/',
            'children': [c.sidebar_entry for c in self.assignments]
        }

    @property
    def assignments(self):
        for a in self.ld['assignments']:
            yield Assignment(self, a)

    def __str__(self):
        return f"Lesson: {self.title} dir={self.dir_name}"


class LessonPlan:

    def __init__(self, less_plan_dir, web_src_dir, less_subdir='lessons'):
        """ Create a new lesson plan

        Args:
            less_plan_dir: Root dir for the lesson plan and other files.
            web_src_dir: The source dir for vuepress files, usually 'docs/src'
            less_subdir: subdir in web_src_dir for generated lesson files.

        """

        self.less_plan_dir = Path(less_plan_dir)
        self.lesson_plan_file = self.less_plan_dir / 'lesson-plan.yaml'
        self.lesson_plan = yaml.safe_load(self.lesson_plan_file.read_text())
        self.web_src_dir = web_src_dir
        self.less_subdir = less_subdir

    @property
    def lessons(self):
        for lesson_key, lesson in self.lesson_plan['lessons'].items():
            yield Lesson(self, lesson)

    def update_config(self, root_dir):
        """Generate the config file for viuepress"""

        lp = self.lesson_plan

        # Read the config from the lesson plan
        config = yaml.safe_load((self.less_plan_dir / 'config.yml').read_text())

        config['title'] = lp['title']
        config['description'] = lp['description']

        # config output file for vuepress
        config_file =  self.web_src_dir / '.vuepress/config.yml'

        config['themeConfig']['sidebar'] = self.make_sidebar(root_dir)

        config_file.write_text(yaml.dump(config))

    def write_dir(self, root_dir: Path = None):
        """Write the lesson plan to the root directory

        Args:
            root_dir (Path): The root directory to write the lesson to
        """

        for page in self.lesson_plan['pages']:
            page_file = self.less_plan_dir / page
            dest_file = self.web_src_dir / page

            shutil.copy(page_file, dest_file)


        assets_dir = self.web_src_dir / '.vuepress/public/assets'
        if not assets_dir.exists():
            assets_dir.mkdir()

        for resource in self.lesson_plan['resources']:
            res_file = self.less_plan_dir / 'assets' / resource
            dest_file = assets_dir / resource

            shutil.copy(res_file, dest_file)

    def build(self, root_dir: Path = None):
        """Write the lesson plan to the root directory

        Args:
            root_dir (Path): The root directory to write the lesson to
        """

        if root_dir is None:
            root_dir = self.web_src_dir / self.less_subdir

        logger.info(f'Writing lesson plan to {root_dir}')

        self.write_dir(root_dir)

        for lesson in self.lessons:
            logger.debug(f'Writing {lesson}')
            lesson.write_dir(root_dir)

        self.update_config(root_dir)

    def make_sidebar(self, root_dir=None):


        return (self.lesson_plan['sidebar']+[l.sidebar_entry for l in self.lessons])
