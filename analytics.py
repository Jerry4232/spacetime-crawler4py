# analytics.py
import re
import os
import json

from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from urllib.parse import urlparse, urldefrag


STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am",
    "an", "and", "any", "are", "aren't", "as", "at", "be", "because",
    "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
    "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "let's", "me", "more", "most",
    "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll",
    "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's",
    "where", "where's", "which", "while", "who", "who's", "whom", "why",
    "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}


class Analytics:
    def __init__(self):
        self.unique_urls = set()
        self.word_counts = Counter()
        self.subdomain_urls = defaultdict(set)
        self.longest_page_url = None
        self.longest_page_word_count = 0

        self.report_dir = "report"
        self.report_path = os.path.join(self.report_dir, "analytics.json")
        os.makedirs(self.report_dir, exist_ok=True)

    def get_plain_text(self, html_content):
        soup = BeautifulSoup(html_content, "lxml")

        # remove non-human text
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)

    def tokenize(self, text):
        words = re.findall(r"[a-zA-Z]+", text.lower())
        return [w for w in words if w not in STOP_WORDS and len(w) > 1]

    def process_page(self, url, html_content):
        url, _ = urldefrag(url)
        if url in self.unique_urls:
            return
        
        self.unique_urls.add(url)
        plain_text = self.get_plain_text(html_content)
        words = self.tokenize(plain_text)

        # top 50 words
        self.word_counts.update(words)

        # longest page
        word_count = len(re.findall(r"[a-zA-Z]+", plain_text.lower()))
        if word_count > self.longest_page_word_count:
            self.longest_page_url = url
            self.longest_page_word_count = word_count

        # subdomain count
        subdomain = urlparse(url).netloc.lower()
        self.subdomain_urls[subdomain].add(url)

        if len(self.unique_urls) % 500 == 0:
            self.write_report()

    def write_report(self):
        data = {
            "unique_pages": len(self.unique_urls),
            "longest_page": {
                "url": self.longest_page_url,
                "word_count": self.longest_page_word_count
            },
            "top_50_words": self.word_counts.most_common(50),
            "subdomains": {
                subdomain: len(urls)
                for subdomain, urls in sorted(self.subdomain_urls.items())
            }
        }

        with open(self.report_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def print_report(self):
        self.write_report()
        print("Unique pages:", len(self.unique_urls))

        print("Longest page:")
        print(self.longest_page_url, self.longest_page_word_count)

        print("Top 50 words:")
        for word, count in self.word_counts.most_common(50):
            print(word, count)

        print("Subdomains:")
        for subdomain in sorted(self.subdomain_urls):
            print(subdomain + ",", len(self.subdomain_urls[subdomain]))
