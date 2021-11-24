# -*- coding: utf-8 -*-
import textwrap

import click
from .. import config

from . import library

import bibman as bibman_l
import bibman.library as libby

if bibman_l.in_library():
    lib = libby.Library()
else:
    lib = None

def parse_provider(record):
    if "arxiv:" in record:
        from bibman.providers.arxiv import Arxiv
        return Arxiv(record.split("arxiv:")[1])

@click.group()
def bibman(args=None):
    """Console script for bibman"""


@bibman.command()
def status():
    if lib:
        click.echo(click.style("Name", bold=True, fg="green") +"\t" + lib.metadata['name'])
    pass


bibman.add_command(library.init)

@click.argument("record")
@bibman.command()
def add(record):
    if lib:
        record_object = parse_provider(record)
        lib.add_record(record_object)
    #click.echo_via_pager(textwrap.fill(record_object.get_abstract()))

@click.argument("record")
@bibman.command()
def show(record):
    if lib:    
        click.echo(lib.records[record.replace(":", ".")])

@click.argument("record")
@bibman.command()
def download(record):
    record_object = parse_provider(record)
    record_object.download()
    
if __name__ == "__main__":

    
    bibman()
