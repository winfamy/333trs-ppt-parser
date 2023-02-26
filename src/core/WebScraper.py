import re
from bs4 import BeautifulSoup
import urllib.request


class WebScraper:
    def __init__(self, url: str) -> None:
        self.url = url

    def fetch_html(self):
        return urllib.request.urlopen(self.url).read()

    def get_readable_text_from_html(self, html):
        """
        https://stackoverflow.com/a/44611484
        """
        soup = BeautifulSoup(html, features="lxml")
        INVISIBLE_ELEMS = ('style', 'script', 'head', 'title')
        RE_SPACES = re.compile(r'\s{3,}')

        text = ' '.join([
            s for s in soup.strings
            if s.parent.name not in INVISIBLE_ELEMS
        ])
        # collapse multiple spaces to two spaces.
        return RE_SPACES.sub('  ', text)
