from httpx import HTTPTransport
from swiftshadow import QuickProxy

from yars2.client import RedditScraper

SEARCH_TERMS = ["Udlændinge"]

proxy = QuickProxy()
if proxy is None:
    exit(1)

transport = {
    f"{proxy.protocol}://": HTTPTransport(
        proxy=proxy.as_string(),
        retries=5,
    ),
}
scraper = RedditScraper(mounts=transport)
for term in SEARCH_TERMS:
    search_result = scraper.search(SEARCH_TERMS[0], limit=100)
