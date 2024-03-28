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


def get_didgets(num):
    return float(str(num)[0:9])


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    random_num = random.random()
    my_dict = {}
    corpus_dict = corpus
    if random_num < damping_factor:
        num_links = len(corpus_dict[page])
        for key in corpus_dict.keys():
            my_dict[key] = get_didgets((1 - damping_factor) / len(corpus_dict.keys()))
        for link in corpus_dict[page]:
            my_dict[link] = get_didgets(((damping_factor * (1 / num_links))) + (1 - damping_factor) / len(corpus_dict.keys()))
    else:
        for key in corpus_dict.keys():
            my_dict[key] = 0
        random_key = random.choice(list(corpus_dict.keys()))
        my_dict[random_key] = 1

    return my_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


    sample = []
    my_dict = {}
    for times in range(n):
        if times == 0:
            random_page = random.choice(list(corpus.keys()))
            sample_transition = transition_model(corpus=corpus,page=random_page,damping_factor=damping_factor)
        while True:
            random_num = random.random()
            key = random.choice(list(sample_transition.keys()))
            if sample_transition[key] > random_num:
                sample_transition = transition_model(corpus=corpus,page=key,damping_factor=damping_factor)
                sample.append(key)
                break
    for key in set(sample):
        my_dict[key] = sample.count(key) / n

    return my_dict


def num_links(corpus):
    corpus_dict = corpus
    links = {}
    for key in corpus_dict.keys():
        links[key] = []
    for key in corpus_dict.keys():
        for page in corpus_dict.keys():
            if key in corpus_dict[page]:
                links[key].append(page)
    return links


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_dict = corpus
    my_dict = {}
    linked_pages = num_links(corpus)
    for key in corpus_dict.keys():
        my_dict[key] = (1 - damping_factor) / len(corpus_dict)
    for i in range(100):
        for linked in linked_pages:
            sum_rank = 0
            for page in linked_pages[linked]:
                sum_rank +=  damping_factor * (my_dict[page] / len(corpus_dict[page]))
            my_dict[linked] = sum_rank + (1 - damping_factor) / len(corpus_dict)

    return my_dict



if __name__ == "__main__":
    main()
 