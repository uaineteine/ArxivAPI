print("[arxiv_paper] importing libraries")
import re
from bs4 import BeautifulSoup
import requests

class Paper:
    def __init__(self, id):
        if not re.match(r'\d{4}\.\d{1,2}', id):
            raise ValueError("ID is not in the correct format. Expected format is \d{4}.\d{1,2}")
        self.id = id

    def __str__(self):
        return f"Title: {self.title}\nAbstract: {self.abstract}"
    
    def getURL(self):
        return(f"https://arxiv.org/abs/{self.id}")
    
    def extract_using_soup(self):
        # Fetch the HTML content from the URL
        response = requests.get(self.getURL())
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the title
        title = soup.find("h1", class_="title mathjax")
        self.title = title.text.split(":", 1)[1].strip()

        # Extract the abstract
        abstract = soup.find("blockquote", class_="abstract mathjax")
        self.abstract = abstract.text.split(":", 1)[1].strip()
