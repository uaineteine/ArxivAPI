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

def parse_xml(xml_text):
    # Parse the XML text
    root = ET.fromstring(xml_text)

    # Define the namespace
    ns = {'ns': 'http://www.w3.org/2005/Atom'}

    # Find all 'entry' tags
    entries = root.findall('.//ns:entry', ns)

    # For each 'entry', get all its children
    entry_xmls = [ET.tostring(entry, encoding='unicode') for entry in entries]

    return entry_xmls
