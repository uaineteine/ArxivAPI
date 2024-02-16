print("[extract_arxiv] importing libraries")
import requests
from bs4 import BeautifulSoup

def extract_paper_info(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the title
    title = soup.find("h1", class_="title mathjax")
    title_text = "Title: " + title.text.split(":", 1)[1].strip()

    # Extract the abstract
    abstract = soup.find("blockquote", class_="abstract mathjax")
    abstract_text = "Abstract: " + abstract.text.split(":", 1)[1].strip()

    # Return the concatenated title and abstract
    return title_text + "\n" + abstract_text
