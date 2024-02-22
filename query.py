# example URL
# https://export.arxiv.org/api/query?search_query=all:the&id_list=1802.06593,0704.0003&start=0&max_results=100

print("[ArxivAPI::query] importing libraries")
import requests
import pandas as pd

def page_query_url(base_query, startIndex, pgSize = 100):
  return f"{base_query}&start={startIndex}&max_results={pgSize}"

def build_base_query_url(idlist):
  comma_ids = ",".join(idlist) #make into a comma separated list
  return f"https://export.arxiv.org/api/query?&id_list={comma_ids}"

def extend_query_with_search(base_query, search_terms):
  return f"{base_query}&search_query=all:{search_terms}"

def xml_query(url_in):
  r = requests.get(url_in)
  return r.text

import xml.etree.ElementTree as ET
from io import StringIO

def parse_entries_to_df(xml_string_array):
# Initialize empty list to hold dictionaries
    data = []

    # Parse each XML string in the array
    for xml_string in xml_string_array:
        # Parse XML string into an ElementTree
        tree = ET.parse(StringIO(xml_string))
        root = tree.getroot()

        # Extract data for each column
        url = root.find("{http://www.w3.org/2005/Atom}id").text
        id = id = url.split('/')[-1]
        updated = root.find("{http://www.w3.org/2005/Atom}updated").text
        published = root.find("{http://www.w3.org/2005/Atom}published").text
        title = root.find("{http://www.w3.org/2005/Atom}title").text
        summary = root.find("{http://www.w3.org/2005/Atom}summary").text

        # Extract author names and join them with a semicolon
        authors = root.findall("{http://www.w3.org/2005/Atom}author")
        author_names = ";".join([author.find("{http://www.w3.org/2005/Atom}name").text for author in authors])

        # Add data to list as a dictionary
        data.append({"id": id, "updated": updated, "published": published, "title": title, "summary": summary, "authors": author_names})

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    return df

def parse_arxiv_xml(xml_text):
    # Parse the XML text
    root = ET.fromstring(xml_text)
    # Define the namespace
    ns = {'ns': 'http://www.w3.org/2005/Atom'}
    # Find all 'entry' tags
    entries = root.findall('.//ns:entry', ns)
    # For each 'entry', get all its children
    entry_xmls = [ET.tostring(entry, encoding='unicode') for entry in entries]
    df = parse_entries_to_df(entry_xmls)
    return df
