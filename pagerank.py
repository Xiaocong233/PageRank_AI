import os
import random
import re
import sys

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
    # initialize probability distribution dictionary
    pd = dict()
    numPages = len(corpus)
    numLinks = len(corpus[page])

    # if empty set, that is, there is no link to other pages
    if corpus[page] == set():
        # set probability distribution of all the web pages to averaged random selection (out of all pages) probability
        for link in corpus:
            pd[link] = (1-damping_factor)/numPages
    else:
        for link in corpus:
            # links to other page gets probability of random selection within the all other links with damping factor
            if link in corpus[page]:
                pd[link] = damping_factor/numLinks + (1-damping_factor)/numPages
            # if not link then gets probability of random selection within all webpages
            else:
                pd[link] = (1-damping_factor)/numPages

    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize dictionaries to store the frequency of each page and its pageRank
    timeAppearance = dict()
    pageRank = dict()
    for page in corpus:
        timeAppearance[page] = 0

    # the starting sample will be randomly selected from all webpages
    initial_sample = random.choice(list(corpus))
    # update frequency
    timeAppearance[initial_sample] += 1

    # remember the initial sample
    last_sample = initial_sample

    # repeat sampling over n times
    for i in range(1, n+1):
        # return the next page based on the weighted random selection with the transition model of last sample
        next_sample = random.choices(list(corpus), 
                      list(transition_model(corpus, last_sample, damping_factor).values())).pop()
        # update frequency
        timeAppearance[next_sample] += 1
        # remember the new sample and prepare to calculate for the next sample
        last_sample = next_sample

    # calculate for pagerank
    for page in corpus:
        pageRank[page] = timeAppearance[page]/n

    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = dict()
    oldPageRank = dict()
    link_to_page = dict()
    numPages = len(corpus)
    numLinks = dict()

    for page in corpus:
        # initialize current and previous page rank to 1/N
        pageRank[page] = 1/numPages
        oldPageRank[page] = 1/numPages

        # initialize all values inside link_to_page to be empty lists
        link_to_page[page] = []

        # get the number of links on page
        numLinks[page] = len(corpus[page])

    # store pages that link TO each pages
    for page in corpus:
        for page2 in corpus:
            # ignore the same webpage
            if page == page2:
                continue
            for link in corpus[page]:
                if link == page2:
                    link_to_page[page2].append(page)

    # initilize delta to be a major value to ensure loop will run
    delta = 10000
    # run iterative algorithm until convergence
    while abs(delta) > 0.001:
        for page in corpus:
            sum = 0
            for link in link_to_page[page]:
                sum += pageRank[link] / numLinks[link]
            pageRank[page] = (1-damping_factor)/numPages + damping_factor*sum
            delta = pageRank[page] - oldPageRank[page]
            oldPageRank[page] = pageRank[page]
    
    # return page ranks
    return pageRank
        

if __name__ == "__main__":
    main()
