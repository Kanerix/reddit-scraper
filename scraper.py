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
    for _ in range(100):
        search = scraper.search(SEARCH_TERMS[0], limit=1)
        pprint(search)
        comments = scraper.comments("Denmark", "1dxb6vp/24årig_anholdt_for_at_køre_ræs_inden_dødsulykke", limit=1)
        pprint(comments)
        break
