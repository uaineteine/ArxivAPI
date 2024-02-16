import requests
from bs4 import BeautifulSoup

# Specify the URL you want to extract text from
target_url = "https://arxiv.org/abs/2207.07456"

# Fetch the HTML content from the URL
response = requests.get(target_url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract the title
title = soup.find("h1", class_="title mathjax")
print("Title:", title.text.split(":", 1)[1].strip())

# Extract the abstract
abstract = soup.find("blockquote", class_="abstract mathjax")
print("Abstract:", abstract.text.split(":", 1)[1].strip())
