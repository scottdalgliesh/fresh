from pathlib import Path
import shutil

import click

ROOT = Path(__file__).parent.parent


@click.command()
@click.argument('name')
def fresh(name: str):
    """Generate blank python project structure."""
    # copy directory structure from this package
    dest = shutil.copytree(
        src=ROOT,
        dst=Path.cwd() / name,
        copy_function=shutil.copy,
        ignore=shutil.ignore_patterns('.git', '*.egg-info', '*__pycache__'))

    # rename files & clear content
    src_dir = (dest / 'fresh').rename(Path(dest / name))
    py_file = (src_dir / 'fresh.py').rename(src_dir / f'{name}.py')
    with open(py_file, 'w') as file:
        file.write('')

    # create blank README
    with open(dest/'README.md', 'w') as file:
        file.write(f'# {name}\n')

    # create setup.py template
    setup_msg = f"""
from setuptools import setup, find_packages

setup(
    name='{name}',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 'package_name',
    ],
    # entry_points='''
    #     [console_scripts]
    #     {name}={name}.<entrypoint_module>:<entrypoint_function>
    # ''',
)
""".lstrip('\n')
    with open(dest/'setup.py', 'w') as file:
        file.write(setup_msg)
