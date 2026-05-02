import re
from urllib.parse import urlparse
from validator import is_valid

def scraper(url, resp):
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
    return list()

if __name__ == "__main__":
    test_urls = [
        "https://www.ics.uci.edu",
        "https://www.google.com",
        "https://www.ics.uci.edu/test.pdf",
        "https://www.ics.uci.edu/a/a/a/a/a/a/a/a/a/a/a"
    ]

    for url in test_urls:
        print(url, is_valid(url))