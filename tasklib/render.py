from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import re
import tasklib.templates as tmpl
from .trinket import generate_trinket_iframe_src, read_code, trinket, goal_image
import yaml
def strip_html(text):
    return re.sub('<.*?>', '', text) if text else ''

def dict_to_yaml(d):

    if not d:
        return ''
    return yaml.dump(d, allow_unicode=True)


def render(template_name, *args, **kwargs):
    """Render a Jinja2 template"""

    tmpl_dir = Path(tmpl.__file__).parent

    env = Environment(loader=FileSystemLoader(tmpl_dir))
    env.filters['strip_html'] = strip_html
    env.globals['trinket'] = trinket
    env.globals['goal_image'] = goal_image
    env.globals['read_code'] = read_code
    env.filters['yaml'] = dict_to_yaml

    if 'content' in kwargs:
        kwargs['content'] = env.from_string(kwargs['content']).render(*args, **kwargs)

    template = env.get_template(template_name)

    return template.render(*args, **kwargs)