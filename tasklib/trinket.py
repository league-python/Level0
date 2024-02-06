import urllib.parse
from pathlib import Path
from jinja2 import pass_context

def read_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()


@pass_context
def goal_image(context, file):

    path = Path(context['working_directory']) / file

    return f'<img src="path" alt="Your Goal" style="float: right; width: 200px; margin-bottom:20px; "/>)'

def generate_trinket_iframe_src(file, working_dir='.', embed_type='python', width='300', height='500'):
    """
    Generates the URL for a Trinket.io embed.

    Parameters:
    - code (str): The code to be executed within the Trinket embed.
    - embed_type (str): The type of Trinket embed (e.g., 'python').
    - width (str): The width of the iframe (default is '300', can be specified in pixels or percentage).
    - height (str): The height of the iframe (default is '500').

    Returns:
    - str: The URL for the Trinket embed.
    """

    code = read_code(Path(working_dir) / file)

    encoded_code = urllib.parse.quote(code.strip())
    return f"https://trinket.io/tools/1.0/jekyll/embed/{embed_type}#code={encoded_code}"

@pass_context
def trinket(context, file,  embed_type='python', width='300', height='500'):
    """
    Generates an HTML iframe for a Trinket.io embed.
    """
    iframe_src = generate_trinket_iframe_src(file, context['working_directory'], embed_type, width, height)
    return f'<iframe width="{width}" height="{height}" src="{iframe_src}" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>'


def generate_trinket_iframe(code, width='300', height='500', embed_type='python'):
    """
    Generates an HTML iframe for a Trinket.io embed.

    Parameters:
    - code (str): The code to be executed within the Trinket embed.
    - width (str): The width of the iframe (default is '300', can be specified in pixels or percentage).
    - height (str): The height of the iframe (default is '500').
    - embed_type (str): The type of Trinket embed (e.g., 'python').

    Returns:
    - str: An HTML iframe element as a string.
    """
    # Corrected base URL
    base_url = 'https://trinket.io/tools/1.0/jekyll/embed/'
    # Ensure the code is URL-encoded to be safely included in the URL
    encoded_code = urllib.parse.quote(code.strip())

    # Construct the src URL
    src_url = f'{base_url}{embed_type}#code={encoded_code}'

    # Construct and return the iframe HTML string
    iframe_html = f'<iframe width="{width}" height="{height}" src="{src_url}" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>'

    return iframe_html
