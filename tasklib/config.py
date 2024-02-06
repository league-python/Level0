""" Reading configuration files
"""

import os
from pathlib import Path

import yaml


def get_config():
    """Read configuration from the _config.yaml file"""
    with open(Path.cwd().joinpath('_config.yml')) as file:
        config = yaml.safe_load(file)

    config['tasks']['module_source'] = os.environ.get('MODULE_SOURCE', None)

    return config


def get_lesson_plan():
    """Read lesson plan from the lesson_plan.yaml file"""
    with open(Path.cwd().joinpath('lesson-plan.yaml')) as file:
        lesson_plan = yaml.safe_load(file)

    return lesson_plan
