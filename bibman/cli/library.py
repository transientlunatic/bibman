"""
Project management tools.
"""
import os

from ..library import Library

import click

@click.command()
@click.argument("name")
@click.option("--root", default=os.getcwd(),
              help="Location to create the project, default is the current directory.")
def init(name, root):
    """
    Roll-out a new library.
    """
    Library.create(name, root)

