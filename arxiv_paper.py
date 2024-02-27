print("[arxiv_paper] importing libraries")
import re
from bs4 import BeautifulSoup
import requests

def summaryText(title, abs):
    return f"Title: {title}\nAbstract: {abs}"

class Paper:
    def __init__(self, id):
        if not re.match(r'\d{4}\.\d{4,5}', id):
            raise ValueError("ID is not in the correct format. Expected format is \d{4}\.\d{4,5}")
        self.id = id
        self.title = ""
        self.abstract = ""

    def __str__(self):
        return summaryText(self.title, self.abstract)
    
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
