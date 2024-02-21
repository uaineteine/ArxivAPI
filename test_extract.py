import arxiv_paper

p = arxiv_paper.Paper("0704.0003")
p.extract_using_soup()
print(p)
