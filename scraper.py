from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from validator import is_valid, is_valid_response
from analytics import Analytics
from similarity import exact_duplicate, near_duplicate

from threading import Lock

duplicate_lock = Lock()
analytics_lock = Lock()

ANALYTICS = Analytics()

seen_hashes = set()
seen_fps = []

def scraper(url, resp):
    if not is_valid_response(resp):
        return []
    
    content_bytes = resp.raw_response.content
    if len(content_bytes) > 5_000_000:
        return []

    try:
        raw_url = getattr(resp.raw_response, "url", None)
        resp_url = getattr(resp, "url", None)
        page_url = urldefrag(raw_url or resp_url or url)[0]
        if not is_valid(page_url):
            return []
        content = content_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return []
    
    with duplicate_lock:
        if exact_duplicate(content, seen_hashes):
            return []
        if near_duplicate(content, seen_fps, threshold=0.97):
            return []
        
    with analytics_lock:
        ANALYTICS.process_page(page_url, content_bytes)
        
    links = extract_next_links(page_url, resp)
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

    result_links = set()

    try:
        content = resp.raw_response.content
        raw_url = getattr(resp.raw_response, "url", None)
        resp_url = getattr(resp, "url", None)
        page_url = urldefrag(raw_url or resp_url or url)[0]
        soup = BeautifulSoup(content, "lxml")
    except Exception:
        return []
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")
        if not href:
            continue
        href = href.strip()
        if href.startswith(("mailto:", "javascript:", "tel:")):
            continue
        absolute_url = urljoin(page_url, href).strip()
        clean_url = urldefrag(absolute_url)[0]
        if is_valid(clean_url):
            result_links.add(clean_url)
    return list(result_links)

