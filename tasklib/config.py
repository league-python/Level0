""" Reading configuration files
"""

import os
from pathlib import Path

import yaml


def get_config(directory='.'):
    """Read configuration from the _config.yaml file"""

    wd = Path(directory)

    with open(Path.cwd().joinpath('lesson-plan.yaml')) as file:
        config = yaml.safe_load(file)

    config['module_source'] = os.environ.get('MODULE_SOURCE', None)

    return config

