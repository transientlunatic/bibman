"""
Functions for the Arxiv Provider
"""

import requests
from bs4 import BeautifulSoup
import click
import textwrap


class Provider:
    pass

class Arxiv(Provider):

    def __init__(self, arxivid):
        """
        Create an Arxiv record from its ID number.
        """

        self.arxivid = arxivid
        self.webpage = None

    def _construct_url(self):
        """
        Construct the URL for the record.
        """

        return f"https://arxiv.org/abs/{self.arxivid}"
        
    def _fetch(self):
        """
        Fetch the web page.
        """

        soup = None

        r = requests.get(self._construct_url())

        if r.status_code == 200:

            soup = BeautifulSoup(r.text, 'html.parser')

            self.webpage = soup
        return soup

    def download(self):
        """
        Download the PDF of this paper.
        """
        url =  f"https://arxiv.org/pdf/{self.arxivid}"
        
        r = requests.get(url)

        if r.status_code == 200:
        
            with open(f"{self.arxivid}.pdf", "wb") as f:
                f.write(r.content)
    
    def get_abstract(self):

        if self.webpage:
            soup = self.webpage
        else:
            soup = self._fetch()
        
        abstract = soup.find(class_="abstract")

        return str(abstract.text).replace("Abstract: ", "").replace("\n", " ")
        
        title = soup.find("h1", class_="title")
