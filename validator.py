import re
from urllib.parse import urlparse

def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        netloc = parsed.netloc.lower()

        if not (
            netloc == "ics.uci.edu" or netloc.endswith(".ics.uci.edu") or
            netloc == "cs.uci.edu" or netloc.endswith(".cs.uci.edu") or
            netloc == "informatics.uci.edu" or netloc.endswith(".informatics.uci.edu") or
            netloc == "stat.uci.edu" or netloc.endswith(".stat.uci.edu")
        ):
            return False

        path = parsed.path.lower()
        query = parsed.query.lower()

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|pps|ppsx|pot|potx|doc|docx|xls|xlsx"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$",
            path
        ):
            return False

        if "doku.php" in path and (
            "backup" in path
            or "backups" in path
            or "history" in path
            or "revision" in path
            or "revisions" in path
            or "diff" in path
            or "restore" in path
        ):
            return False

        if (
            "do=" in query
            or "rev=" in query
            or "sectok=" in query
            or "idx=" in query
            or "replytocom=" in query
            or "share=" in query
            or "ical=" in query
            or "tribe_" in query
            or "filter[" in query
            or "filter%5b" in query
            or "printable=" in query
            or "format=" in query
        ):
            return False

        if "/lib/exe/" in path or "/lib/tpl/" in path:
            return False

        if path.count("/") > 10:
            return False

        parts = [part for part in path.split("/") if part]
        for i in range(len(parts) - 2):
            if parts[i] == parts[i + 1] == parts[i + 2]:
                return False

        if "calendar" in path and ("month=" in query or "year=" in query):
            return False

        if query.count("&") > 3:
            return False

        return True

    except Exception:
        return False