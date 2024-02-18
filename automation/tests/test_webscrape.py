print("[test_webscrape] importing libraries")
import extract_arxiv

url = "https://arxiv.org/abs/2207.07456"
print("[test_webscrape] performing test on " + url)

# Test the function with a sample URL
print(extract_arxiv.extract_paper_info(url))
