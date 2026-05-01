"""
File: analytics.py (Create this new file) 
Goal: Extract text and count stats for the report. 
To-Do:
1.	Get Plain Text: Write a function to strip all HTML tags (like <div>, <script>) 
    from the content to leave only human-readable text.
2.	Word Count: Count the 50 most common words, ignoring "stop words" 
    (like "the", "is", "at").
3.	Subdomain Count: Track how many unique URLs belong to each subdomain 
    (e.g., vision.ics.uci.edu vs wics.ics.uci.edu).
"""
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urlparse
from collections import defaultdict

def get_plain_text(html_content):
    """
    Strip HTML tags from the content to get plain text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def count_common_words(text, stop_words):
    """
    Count the 50 most common words in the text, ignoring stop words.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(50)

def count_subdomains(urls):
    """
    Count how many unique URLs belong to each subdomain.
    """
    subdomain_counts = defaultdict(set)
    for url in urls:
        parsed_url = urlparse(url)
        subdomain = parsed_url.netloc
        subdomain_counts[subdomain].add(url)
    return {subdomain: len(urls) for subdomain, urls in subdomain_counts.items()}

# Example usage:
if __name__ == "__main__":
    html_content = "<html><body><h1>Example Page</h1><p>This is an example page.</p></body></html>"
    stop_words = set(["the", "is", "at", "which", "on", "and"])
    
    plain_text = get_plain_text(html_content)
    print("Plain Text:", plain_text)
    
    common_words = count_common_words(plain_text, stop_words)
    print("Common Words:", common_words)
    
    urls = ["http://vision.ics.uci.edu/page1", "http://vision.ics.uci.edu/page2", 
            "http://wics.ics.uci.edu/page1"]
    subdomain_counts = count_subdomains(urls)
    print("Subdomain Counts:", subdomain_counts)
