# analytics.py

from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from urllib.parse import urlparse, urldefrag
import re


class Analytics:
    def __init__(self):
        self.unique_urls = set()
        self.word_counts = Counter()
        self.subdomain_urls = defaultdict(set)
        self.longest_page_url = None
        self.longest_page_word_count = 0

        self.stop_words = set([
            "the", "is", "at", "which", "on", "and", "a", "an", "of",
            "to", "in", "for", "with", "by", "as", "from", "that",
            "this", "it", "be", "are", "was", "were", "or", "but"
        ])

    def get_plain_text(self, html_content):
        soup = BeautifulSoup(html_content, "lxml")

        # remove non-human text
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)

    def tokenize(self, text):
        words = re.findall(r"[a-zA-Z]+", text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 1]

    def process_page(self, url, html_content):
        # normalize URL by removing #fragment
        url, _ = urldefrag(url)

        # avoid double counting same page
        if url in self.unique_urls:
            return

        self.unique_urls.add(url)

        text = self.get_plain_text(html_content)
        words = self.tokenize(text)

        # top 50 words across ALL pages
        self.word_counts.update(words)

        # longest page
        if len(words) > self.longest_page_word_count:
            self.longest_page_url = url
            self.longest_page_word_count = len(words)

        # subdomain count
        subdomain = urlparse(url).netloc.lower()
        self.subdomain_urls[subdomain].add(url)

    def print_report(self):
        print("Unique pages:", len(self.unique_urls))

        print("Longest page:")
        print(self.longest_page_url, self.longest_page_word_count)

        print("Top 50 words:")
        for word, count in self.word_counts.most_common(50):
            print(word, count)

        print("Subdomains:")
        for subdomain in sorted(self.subdomain_urls):
            print(subdomain + ",", len(self.subdomain_urls[subdomain]))
            