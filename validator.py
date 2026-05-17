# validator.py
"""
low-information rule: 
file extensions, login/comment/reply/restore pages, 
calendars, revision/history/diff pages, 
repeated path components, deep paths, slide/page families, 
genealogy/helpdesk traps, and near-duplicate text families. 
"""


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
        
        BAD_SUBDOMAINS = {
            "intranet.ics.uci.edu",
            "password.ics.uci.edu",
            "checkin.ics.uci.edu",
            "myip.ics.uci.edu",
            "speedtest.ics.uci.edu",
            "signage.ics.uci.edu",
        }

        if netloc in BAD_SUBDOMAINS:
            return False

        path = parsed.path.lower()
        query = parsed.query.lower()

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|pps|ppsx|pot|potx|doc|docx|xls|xlsx"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|ova|vmdk|qcow2"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|xml|rss|atom|log|txt"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|py|java|cpp|c|h|hpp|cs|ts|go|rb)$",
            path
        ):
            return False
        
        bad_login_terms = ["login", "register", "restore"]
        bad_photo_terms = ["/pix/", "/gallery/"]
        bad_terms = bad_login_terms + bad_photo_terms
        
        if any(term in path or term in query for term in bad_terms):
            return False
        
        if path.count("/") > 10:
            return False
            
        date_sep = r"[-/._]"
        date_patterns = [
            rf"\d{{4}}{date_sep}\d{{1,2}}{date_sep}\d{{1,2}}",  # YYYY-MM-DD
            rf"\d{{1,2}}{date_sep}\d{{1,2}}{date_sep}\d{{4}}",  # MM-DD-YYYY
            rf"(fall|winter|spring|summer){date_sep}\d{4}{date_sep}week{date_sep}\d+" # fall-2023-week-10
        ]
        for pattern in date_patterns:
            if re.search(pattern, path) or re.search(pattern, query):
                return False

        if "calendar" in path and ("month=" in query or "year=" in query):
            return False

        if query.count("&") > 3:
            return False
        
        parts = [part for part in path.split("/") if part]
        for i in range(len(parts) - 2):
            if parts[i] == parts[i + 1] == parts[i + 2]:
                return False
        
        if any(trap_pattern in query for trap_pattern in [
            "action=diff",
            "action=history",
            "version=",
        ]):
            return False
        
        if "/~irus/twist/" in path and "/presentations/" in path:
            return False

        if re.search(r"/(?:tsld|sld|slide|page)[-_]?\d+\.html?$", path):
            return False
        
        if re.search(r"/page/\d+/?", path):
            m = re.search(r"/page/(\d+)/?", path)
            # Exclude paginated pages beyond page 3
            if m and int(m.group(1)) > 3:
                return False
            
        if path.startswith("/~"):
            # professor profile like eppstein, thornton, dechter, wscacchi etc. 
            # often have deep paths
            parts = [p for p in path.split("/") if p]
            if len(parts) > 2:
                return False
        
        if netloc == "ics.uci.edu" and path.startswith("/~dhirschb/genealogy/"):
            return False
        
        # open tickets in ics helpdesk
        if netloc == "helpdesk.ics.uci.edu" and path.startswith("/ticket/"):
            return False

        if "doku.php" in path and (
            "backup" in path
            or "backups" in path
            or "history" in path
            or "revision" in path
            or "revisions" in path
            or "diff" in path
            or "restore" in path
            or "idx=" in query
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

        return True

    except Exception:
        return False
    

def is_valid_response(resp):
    return(
        resp is not None
        and resp.status == 200
        and resp.raw_response is not None
        and resp.raw_response.content is not None
        and len(resp.raw_response.content) > 0
    )

