import frontmatter

import yaml
from pathlib import Path
from slugify import slugify
import shutil

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


class Assignment:
    def __init__(self, src_dir,lesson_data, assignment_dir):
        self.ld = lesson_data
        self.adir = assignment_dir
        self.src_dir = src_dir


class Lesson:

    def __init__(self, src_dir, lesson_data):
        self.ld = lesson_data
        self.src_dir = src_dir

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

        shutil.copy(self.src_dir /self.ld['text'] , lesson_dir / 'index.md')

        return lesson_dir

    def __str__(self):
        return f"Lesson: {self.title} dir={self.dir_name}"

class LessonPlan:

    def __init__(self,  lesson_dir):
        self.lesson_dir = Path(lesson_dir)
        self.lesson_plan_file = self.lesson_dir / 'lesson-plan.yaml'

        self.lesson_plan = yaml.safe_load(self.lesson_plan_file.read_text())

    @property
    def lessons(self):
        for lesson_key, lesson in self.lesson_plan['lessons'].items():
            yield Lesson(self.lesson_dir, lesson)

