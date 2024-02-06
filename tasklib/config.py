""" Reading configuration files
"""

import os
from pathlib import Path

import yaml


def update_config(root_dir, sidebar):

    config_file = root_dir / '.vuepress/config.yml'

    config = yaml.safe_load(config_file.read_text())

    config['themeConfig']['sidebar'] = sidebar

    config_file.write_text(yaml.dump(config))



