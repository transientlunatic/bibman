"""
Functions for the Arxiv Provider
"""

import requests
from bs4 import BeautifulSoup
import click
import textwrap
import os


class Provider:
    pass

class Arxiv(Provider):

    def __init__(self, arxivid):
        """
        Create an Arxiv record from its ID number.
        """

        self.arxivid = arxivid
        self.record_id = f"arxiv.{self.arxivid}"
        self.webpage = None

        self.metadata = {}

    def _construct_url(self):
        """
        Construct the URL for the record.
        """

        return f"https://arxiv.org/abs/{self.arxivid}"
        
    def _fetch(self):
        """
        Fetch the web page.
        """
        if not self.webpage:
            soup = None

            r = requests.get(self._construct_url())

            if r.status_code == 200:

                soup = BeautifulSoup(r.text, 'html.parser')

                self.webpage = soup
            return soup
        else:
            return self.webpage
        
    def parse(self):
        soup = self._fetch()
        
        abstract = soup.find(class_="abstract")
        title = soup.find("h1", class_="title")

        self.metadata['title'] = title.text
        self.metadata['arxivid'] = self.arxivid

        authors = soup.find("div", class_="authors").text.replace("Authors:", "").split(", ")
        
        self.metadata['authors'] = authors

    def download_pdf(self, root=os.getcwd()):
        """
        Download the PDF of this paper.
        """
        url =  f"https://arxiv.org/pdf/{self.arxivid}"
        
        r = requests.get(url)

        if r.status_code == 200:
            with open(os.path.join(root, f"{self.record_id}.pdf"), "wb") as f:
                f.write(r.content)
            with open(os.path.join(root, f"{self.record_id}.abs"), "w") as f:
                f.write(self.get_abstract())
    
    def get_abstract(self):

        if self.webpage:
            soup = self.webpage
        else:
            soup = self._fetch()
        
        abstract = soup.find(class_="abstract")

        return str(abstract.text).replace("Abstract: ", "").replace("\n", " ")
