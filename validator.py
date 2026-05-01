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

        path = parsed.path.lower()

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$",
            path
        ):
            return False

        if path.count("/") > 10:
            return False

        parts = [part for part in path.split("/") if part]
        for i in range(len(parts) - 2):
            if parts[i] == parts[i + 1] == parts[i + 2]:
                return False

        if re.search(r"/\d{4}/\d{1,2}/\d{1,2}", path):
            return False

        if "calendar" in path and ("month=" in parsed.query.lower() or "year=" in parsed.query.lower()):
            return False

        if parsed.query.count("&") > 5:
            return False

        return True

    except TypeError:
        return False