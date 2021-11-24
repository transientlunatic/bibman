import requests
from bs4 import BeautifulSoup
import click
import textwrap

url = "https://arxiv.org/abs/1903.09204"

r = requests.get(url)

if r.status_code == 200:

    soup = BeautifulSoup(r.text, 'html.parser')
    abstract = soup.find(class_="abstract")

    title = soup.find("h1", class_="title")

    click.secho(title.text, bold=True)
    
    click.echo(textwrap.fill(abstract.text.replace("\n", " ")))
