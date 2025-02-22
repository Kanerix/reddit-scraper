from httpx import Client

from yars2.agents import get_agent
from yars2.model import RedditSearch


class RedditScraper(Client):
    def search(
        self, query: str, limit: int = 10, after: str | None = None
    ) -> RedditSearch:
        url = "https://www.reddit.com/search.json"
        params = {
            "q": query,
            "limit": limit,
            "type": "link",
            "sort": "relevance",
        }

        if after is not None:
            params["after"] = after

        res = self.get(url, params=params)
        res.raise_for_status()

        res_json = res.json()

        return RedditSearch.model_validate(res_json)

    def search_subreddit(
        self, subreddit, query, limit: int = 10, after: str | None = None
    ):
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {
            "q": query,
            "limit": limit,
            "sort": "relevance",
            "type": "link",
            "restrict_sr": "on",
        }
        return self.get(url, params=params)

    def get_post(self, permalink: str) -> dict:
        url = f"https://www.reddit.com{permalink}.json"
        res = self.get(url)
        res.raise_for_status()
        return res.json()

    def request(self, *args, **kwargs):
        """Random user agent for each request."""
        self.headers.update({"User-Agent": get_agent()})
        return super().request(*args, **kwargs)
