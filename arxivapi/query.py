# example URL
# https://export.arxiv.org/api/query?search_query=all:the&id_list=1802.06593,0704.0003&start=0&max_results=100

print("[ArxivAPI::query] importing libraries")
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO
import concurrent.futures

ns_url = "http://www.w3.org/2005/Atom"

def page_query_url(base_query, startIndex, pgSize = 200):
  return f"{base_query}&start={startIndex}&max_results={pgSize}"

def build_base_query_url(idlist):
  comma_ids = ",".join(idlist) #make into a comma separated list
  return f"https://export.arxiv.org/api/query?&id_list={comma_ids}"

def extend_query_with_search(base_query, search_terms):
  return f"{base_query}&search_query=all:{search_terms}"

def xml_query(url_in):
  r = requests.get(url_in)
  # Return None if the request failed
  if r.status_code != 200:
    return None
  return r.text

def _parse_entries_to_df(xml_string_array):
    ns = "{" + f"{ns_url}" + "}"
    # Initialize empty list to hold dictionaries
    data = []

    # Parse each XML string in the array
    for xml_string in xml_string_array:
        try:
          #print(xml_string)
          # Parse XML string into an ElementTree
          tree = ET.parse(StringIO(xml_string))
          root = tree.getroot()

  
          # Extract data for each column
          def rfind(name):
            return root.find(f"{ns}{name}").text
          url = rfind("id")
          id_full = url.split('/')[-1]
          id_ver  = id_full.split('v')[-1]
          id      = id_full.split('v')[0]
          updated = url = rfind("updated")
          published = url = rfind("published")
          title = url = rfind("title")
          summary = url = rfind("summary")

          # Extract author names and join them with a semicolon
          authors = root.findall(f"{ns}author")
          author_names = ";".join([author.find(f"{ns}name").text for author in authors])

          # Add data to list as a dictionary
          data.append({"id": id, "ver" : id_ver, "updated": updated, "published": published, "title": title, "summary": summary, "authors": author_names})
        except:
           print("[ArxivAPI::query] Parsing XML failed")

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    return df

def parse_arxiv_xml(xml_text):
    # Parse the XML text
    root = ET.fromstring(xml_text)
    # Find all 'entry' tags
    entries = root.findall('.//ns:entry', {'ns': ns_url})
    # For each 'entry', get all its children
    entry_xmls = [ET.tostring(entry, encoding='unicode') for entry in entries]
    df = _parse_entries_to_df(entry_xmls)
    return df

def _chunkify_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def query_ids(id_list, chunk_size=50, num_workers = 1):
  print("[ArxivAPI::query] extracting id_list")
  chunks = _chunkify_list(id_list, chunk_size) # chunk size of 100, pgsize of 5 times larger as there could be more versions per paper
  
  dfs = []

  def process_chunk(id_chunk):
    q = build_base_query_url(id_chunk)
    q = page_query_url(q, 0, pgSize=chunk_size*5)
    xml = xml_query(q)
    if xml is not None:
      entries_df = parse_arxiv_xml(xml)
      return entries_df

  with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    future_to_df = {executor.submit(process_chunk, id_chunk): id_chunk for id_chunk in chunks}
    for i, future in enumerate(concurrent.futures.as_completed(future_to_df)):
      df = future.result()
      if df is not None:
        dfs.append(df)
      if (i % 4 == 0):
        perc = (i / len(chunks)) * 100
        print(f"[ArxivAPI::query] {perc}% of chunks retrieved")

  # Append entries_df to final_df
  final_df = pd.concat(dfs, ignore_index=True)
  return final_df
