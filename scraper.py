from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from validator import is_valid
from analytics import *

def scraper(url, resp):
    # TODO: delete this section when you want to run the crawler in full
    # Deleted
    # TODO: delete until here

    if not is_valid_response(resp):
        return list()
    
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
        return list()
    
    result_links = []

    try:
        content = resp.raw_response.content
        soup = BeautifulSoup(content, "lxml")
    except Exception:
        return list()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")

        if not href:
            continue

        absolute_url = urljoin(url, href)
        clean_url, _ = urldefrag(absolute_url)
        clean_url = clean_url.strip()

        if clean_url:
            result_links.append(clean_url)

    return list(dict.fromkeys(result_links))

def is_valid_response(resp):
    return (
        resp is not None
        and resp.status == 200
        and resp.raw_response is not None
        and resp.raw_response.content is not None
        and len(resp.raw_response.content) > 0
    )
