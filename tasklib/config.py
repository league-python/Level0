""" Reading configuration files
"""

import os
from pathlib import Path

import yaml


def get_config(root='.'):
    """Read configuration from the _config.yaml file"""

    wd = Path(root)

    with open(Path.cwd().joinpath('lesson-plan.yaml')) as file:
        config = yaml.safe_load(file)

    config['module_source'] = os.environ.get('MODULE_SOURCE', None)
    config['lesson_root'] = wd / 'docs/src/lessons'

    return config

