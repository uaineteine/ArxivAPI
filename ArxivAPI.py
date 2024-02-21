https://export.arxiv.org/api/query?search_query=all:the&id_list=1802.06593,0704.0003&start=0&max_results=100

pgSize = 100

def page_query_url(base_url, startIndex):
  return f"{base_url}&start={startIndex}&max_results={pgSize}"
