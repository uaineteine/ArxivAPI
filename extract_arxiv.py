import requests
from bs4 import BeautifulSoup

# Specify the URL you want to extract text from
target_url = "https://arxiv.org/abs/2207.07456"

# Fetch the HTML content from the URL
response = requests.get(target_url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract all visible text (excluding script, meta, link, and style tags)
for text in soup.body.find_all(string=True):
    if text.parent.name not in ["script", "meta", "link", "style"] and text.strip():
        print(text.strip())
