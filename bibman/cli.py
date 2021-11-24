# -*- coding: utf-8 -*-

import textwrap

import click


def parse_provider(record):
    if "arxiv:" in record:
        from bibman.providers.arxiv import Arxiv
        return Arxiv(record.split("arxiv:")[1])

@click.group()
def bibman(args=None):
    """Console script for bibman"""
    pass

@click.argument("record")
@bibman.command()
def check(record):

    
    record_object = parse_provider(record)
    click.echo_via_pager(textwrap.fill(record_object.get_abstract()))


@click.argument("record")
@bibman.command()
def download(record):

    
    record_object = parse_provider(record)
    record_object.download()
    
if __name__ == "__main__":
    bibman()
