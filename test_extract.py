print("[test_extract] testing extract using soup")
import arxiv_paper

p = arxiv_paper.Paper("0704.0003")
p.extract_using_soup()
print(p)



print("[test_extract] testing extract using API")
import query
q = query.build_base_query_url(["1802.06593", "0704.0003"])
q = query.page_query_url(q, 0)
xml = query.xml_query(q)
print(xml)
