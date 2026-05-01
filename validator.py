import re
from urllib.parse import urlparse

def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        if not (
            parsed.netloc.endswith(".ics.uci.edu") or
            parsed.netloc.endswith(".cs.uci.edu") or
            parsed.netloc.endswith(".informatics.uci.edu") or
            parsed.netloc.endswith(".stat.uci.edu")
        ):
            return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$",
            parsed.path.lower()
        ):
            return False


        if parsed.path.count("/") > 10:
            return False

        parts = parsed.path.split("/")
        if len(parts) != len(set(parts)):
            return False

        if parsed.query.count("&") > 5:
            return False

        return True

    except TypeError:
        return False