import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    total_pages = len(corpus)
    dist = {}
    
    #If page has no links
    if not corpus[page]:                
        for pages in corpus:
            dist[pages] = 1/total_pages
        return dist

    pages_to_go = len(corpus[page])
    for pages in corpus:
        dist[pages] = (1 - damping_factor)/total_pages
    
    for pages in corpus[page]:
        dist[pages] += damping_factor/pages_to_go
    
    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visit_counter={}
    page_rank = {}

    for i in range(n):
        x = random.random()     #Generate a random float between 0 and 1
        if i == 0:      #Initially go to a random page
            visit = random.choice(tuple(corpus))
            visit_counter[visit] = 1
        else:       #Choose a page depending on their probability distribution
            dist = transition_model(corpus,visit,damping_factor)
            for pages in dist:
                if x <= dist[pages]:
                    visit = pages
                    visit_counter.setdefault(visit,0)
                    visit_counter[visit] += 1
                    break
                else:
                    x -= dist[pages]

    for pages in visit_counter:
        page_rank[pages] = visit_counter[pages]/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    total_pages = len(corpus)
    parent = {}
    
    for pages in corpus:
        page_rank[pages] = 1/total_pages
    
    for pages in corpus:
        for page in corpus[pages]:
            parent.setdefault(page, [pages])
            if pages not in parent[page]:
                parent[page].append(pages)

    for pages in corpus:
        if len(corpus[pages]) == 0:     #If a page has no outgoing links
            for page in corpus:
                parent.setdefault(page,[pages])
                parent[page].append(pages)
            
        if pages not in parent:         #If a page does not have a parent page
            parent[pages] = []

    while True:
        
        prev_page_rank = copy.deepcopy(page_rank)

        for pages in corpus:
            page_rank[pages] = (1 - damping_factor)/total_pages
            for parents in parent[pages]:
                if len(corpus[parents])==0:     #If a parent page has no outgoing links
                    num_links = total_pages
                else:
                    num_links = len(corpus[parents])
                page_rank[pages] += damping_factor*(page_rank[parents]/num_links)

        accuracy_check = True
        
        for pages in corpus:
            if abs(page_rank[pages] - prev_page_rank[pages]) > 0.001:
                accuracy_check = False
                break
            
        if accuracy_check:
            return page_rank


if __name__ == "__main__":
    main()
