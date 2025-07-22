print("[arxiv_paper] importing libraries")
import re
from bs4 import BeautifulSoup
import requests

def _format_arxiv_id(year, month, serial, archive=None):
    """
    Returns the correct arXiv ID format based on the date.
    - For pre-April 2007: requires 'archive' (e.g., 'hep-th'), year, month, serial.
    - For post-April 2007: year, month, serial only.
    """
    # arXiv switched to new format in April 2007
    if (year < 2007) or (year == 2007 and month < 4):
        if not archive:
            raise ValueError("Archive (e.g., 'hep-th') required for old-style arXiv IDs.")
        return f"{archive}/{str(year)[-2:]:0>2}{month:0>2}{serial:0>3}"
    else:
        return f"{str(year)[-2:]:0>2}{month:0>2}.{serial:0>4}"

# Examples:
# Old: format_arxiv_id(2006, 12, 123, archive='hep-th') -> 'hep-th/0612123'
# New: format_arxiv_id(2021, 1, 12345) -> '2101.12345'

def _get_max_id_for_date(year, month):
    """
    Returns the maximum number of digits for the serial part of the arXiv ID
    based on the date (format change in April 2007).
    """
    if (year < 2007) or (year == 2007 and month < 4):
        return 5  # Old format: up to 5 digits, but usually 3
    else:
        return 5  # New format: up to 5 digits

def _summaryText(title, abs):
    return f"Title: {title}\nAbstract: {abs}"

class ArxivPaper:
    def __init__(self, id):
        if not re.match(r'\d{4}\.\d{4,5}', id):
            raise ValueError("ID is not in the correct format. Expected format is \d{4}\.\d{4,5}")
        self.id = id
        self.title = ""
        self.abstract = ""

    def __str__(self):
        return _summaryText(self.title, self.abstract)
    
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
