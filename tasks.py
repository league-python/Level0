import os
from pathlib import Path
import shutil
import yaml
from invoke import task
from tasklib import *
from pathlib import  Path

import re

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

	for f in list(path.glob('*.png')) +  list(path.glob('*.gif')):
		meta['resources'].append(f)

	return meta

def write_assignment_text(ad: dict):

	from textwrap import dedent

	if not 'trinket' in ad['texts']:
		return 

	t_width = ad.get('trinket',{}).get('width', 1000)
	t_height = ad.get('trinket',{}).get('height', 800)
	t_type = ad.get('trinket',{}).get('type', 'python')

	file_name = ad['sources'][0].name

	code_block = dedent(f"""
	{{% include trinket-open type='{t_type}' height='{t_height}' width='{t_width}' %}}
	{{% include_relative {file_name} %}}
	{{% include trinket-close %}}
	""").strip()

	text = ad['texts']['trinket'].read_text()

	text = text.replace('<!-- code -->', code_block)

	front_matter = dedent(f"""
	---
	title: {ad['title']}
	
	---
	""").strip()

	return front_matter + "\n" + text

def write_assignment_dir(ad: dict):
	pass



@task
def dev(ctx, directory='.'):
	config = get_config()['tasks']
	ms = Path(config['module_source'])

	lesson_root = Path('lessons')

	lp = get_lesson_plan()
	#print(lp)

	for lesson, assignments in lp.items():

		l_path = lesson_root / lesson

		if not l_path.exists():
			l_path.mkdir(parents=True)

		for assign in assignments:
			meta = get_assignment(ms/assign)

			if 'trinket' in meta['texts']:
				print(f"Writing {l_path}")
				text = write_assignment_text(meta)
				(l_path / 'index.md').write_text(text)

			for f in list(meta['resources']) + list(meta['sources']):
				f = Path(f)
				print(f"Copying {f}")
				shutil.copy(f, l_path / f.name)



