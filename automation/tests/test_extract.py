print("[test_extract] testing extract using soup")
import arxiv_paper

p = arxiv_paper.ArxivPaper("0704.0003")
p.extract_using_soup()
print(p)



print("[test_extract] testing extract using API")
import query
q = query.build_base_query_url(["1802.06593", "0704.0003"])
q = query.page_query_url(q, 0)
xml = query.xml_query(q)
print(xml)
entries = query.parse_arxiv_xml(xml)
print("")
print(entries)

print("[test_extract] testing extract using API for ID that doesn't exist")
import query
q = query.build_base_query_url(["0704.9000"])
q = query.page_query_url(q, 0)
xml = query.xml_query(q)
print(xml)
entries = query.parse_arxiv_xml(xml)
print("")
print(entries)
