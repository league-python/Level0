from invoke import task
from pathlib import Path
import shutil

def create_title(file_name):
	"""Create a readable title by replacing underscores with spaces and capitalizing each word."""
	return ' '.join(word.capitalize() for word in file_name.replace('_', ' ').split())

def python_file_template(py_file_name, title):
	"""Generate the Markdown content for a Python file."""
	return f"""---
layout: default
title: '{title}'
---

{{% include trinket-open type='python' height='800' width='1000' %}}
{{% include_relative {py_file_name} %}}
{{% include trinket-close %}}
"""

def index_md_template(directory_name, links):
	"""Generate the Markdown content for the index file."""
	title = directory_name.replace('_', ' ').title()
	links_md = "\n".join(links)
	return f"""---
layout: default
title: "{title}"
---

# {title}

Let's do some drawing!

{links_md}
"""


def generate_docs_index(docs_dir):
	"""Generate a top-level index.md for the docs/ directory."""

	index_content = """---
layout: default
title: "Level 0, Module 0: Getting Started"
---

# Let's get started learning Python!

"""
	print("Generate the docs index")
	for sub_dir in docs_dir.iterdir():
		if sub_dir.is_dir() and (sub_dir / 'index.md').exists():
			# Add a link to the directory's index.md
			dir_title = sub_dir.name.replace('_', ' ').title()
			index_content += f"\n* [{dir_title}]({{{{ site.baseurl }}}}{{% link {sub_dir.name}/index.md %}})"
			
			# Add links to the Python Markdown files
			for md_file in sub_dir.glob('*.md'):
				if md_file.name != 'index.md':
					md_title = create_title(md_file.stem)
					index_content += f"\n  * [{md_title}]({{{{ site.baseurl }}}}/{sub_dir.name}/{md_file.name.replace('.md', '.html')})"

	# Write the generated index content to the top-level index.md in docs/
	(docs_dir / 'index.md').write_text(index_content)
	print(f"Write index to {docs_dir / 'index.md'}")

def build_recipe_dir(docs_dir, item):

	print(f"Build recipe dir {str(item)}")

	python_files = list(item.glob('*.py'))
	if python_files:
		doc_dir = docs_dir / item.name
		doc_dir.mkdir(parents=True, exist_ok=True)
		
		# Track markdown file names for index
		markdown_links = []

		for py_file in python_files:
			dst_file_path = doc_dir / py_file.name
			md_file_path = doc_dir / (py_file.stem + '.md')
			title = create_title(py_file.stem)
			
			# Copy the Python file
			shutil.copy(py_file, dst_file_path)
			
			# Generate and write the markdown content for the Python file
			md_file_path.write_text(python_file_template(py_file.name, title))

			# Append markdown link to the list
			markdown_links.append(f"* [{title}]({{{{ site.baseurl }}}}/{doc_dir.relative_to(docs_dir)}/{py_file.stem}.html)")

		# Generate and write index.md for the directory
		(doc_dir / 'index.md').write_text(index_md_template(item.name, markdown_links))

@task
def build(ctx):
	root_dir = Path('.')
	docs_dir = root_dir / 'docs'
	docs_dir.mkdir(exist_ok=True)
	
	for item in root_dir.iterdir():
		
		if item.is_dir() and item.name not in ('docs',) and not item.name.startswith('.') and not item.name.startswith('_'):

			build_recipe_dir(docs_dir,item)

		

	generate_docs_index(docs_dir)


@task
def clean_names(ctx, directory='.'):
    """
    Looks for Python files starting with '_' and processes them accordingly.
    
    Args:
    - directory: The root directory to start the search from. Defaults to the current directory.
    """
    root_dir = Path(directory)
    
    # Recursively find all Python files starting with '_'
    for py_file in root_dir.rglob('_*.py'):
        # Delete __init__.py files
        if py_file.name == '__init__.py':
            print(f"Deleting: {py_file}")
            py_file.unlink()
        # Rename other files by removing the leading '_'
        else:
            new_name = py_file.with_name(py_file.name[1:])
            print(f"Renaming: {py_file} to {new_name}")
            py_file.rename(new_name)

