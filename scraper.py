from pprint import pprint
from httpx import HTTPTransport
from swiftshadow import QuickProxy

from reddit_scraper.client import RedditScraper

SEARCH_TERMS = ["Invandrere", "Migranter", "Flygtninge", "Asylansøgere"]

proxy = QuickProxy()
if proxy is None:
    exit("No proxy available.")

transport = {
    f"{proxy.protocol}://": HTTPTransport(
        proxy=proxy.as_string(),
        retries=5,
    ),
}
scraper = RedditScraper(mounts=transport)

for term in SEARCH_TERMS:
    for i in range(100):
        search_result = scraper.search(SEARCH_TERMS[0], limit=100)
        pprint(search_result.model_dump())
