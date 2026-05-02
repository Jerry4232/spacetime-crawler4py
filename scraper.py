from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from validator import is_valid
from analytics import Analytics
from similarity import exact_duplicate, near_duplicate

ANALYTICS = Analytics()

seen_hashes = set()
seen_fps = []


MAX_PAGES = 10   # change this for testing
visited_count = 0

def scraper(url, resp):
    # TODO: delete this section when you want to run the crawler in full
    global visited_count
    if visited_count >= MAX_PAGES:
        return []   # stop expanding frontier
    visited_count += 1
    # TODO: delete until here

    if not is_valid_response(resp):
        return []
    
    content = resp.raw_response.content.decode("utf-8", errors="ignore")

    if exact_duplicate(content, seen_hashes):
        return []
    if near_duplicate(content, seen_fps):
        return []
    
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if not is_valid_response(resp):
        return []

    result_links = []

    try:
        content = resp.raw_response.content
        page_url = resp.raw_response.url
        ANALYTICS.process_page(page_url, content)
        soup = BeautifulSoup(content, "lxml")
    except Exception:
        return []
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")
        absolute_url = urljoin(url, href).strip()
        clean_url = urldefrag(absolute_url)[0]
        result_links.append(clean_url)
    return result_links


def is_valid_response(resp):
    return(
        resp.status == 200
        and resp.raw_response is not None
        and resp.raw_response.content is not None
        and len(resp.raw_response.content) > 0
    )
