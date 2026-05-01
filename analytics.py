# analytics.py

from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from urllib.parse import urlparse, urldefrag
import re


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
