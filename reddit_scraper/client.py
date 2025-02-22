from typing import Literal, override

from httpx import Client

from reddit_scraper.agents import get_agent
from reddit_scraper.model import RedditListing


class RedditScraper(Client):
    """https://www.reddit.com/dev/api"""

    @override
    def request(self, *args, **kwargs):
        """Random user agent for each request."""
        self.headers.update({"User-Agent": get_agent()})
        return super().request(*args, **kwargs)

    def search(
        self,
        query: str,
        after: str | None = None,
        before: str | None = None,
        count: int = 0,
        limit: int = 25,
        category: str | None = None,
        kind: Literal["sr", "link", "user"] = "link",
        sort: Literal["relevance", "new", "hot", "top", "comments"] = "relevance",
        show: Literal["all"] | None = None,
    ) -> RedditListing:
        if len(query) > 512:
            raise ValueError("Query too long, max 512 characters.")
        if limit > 100:
            raise ValueError("Limit too high, max 100.")
        if category and len(category) > 5:
            raise ValueError("Category too long, max 5 characters.")

        url = "https://www.reddit.com/search.json"
        params = {
            "q": query,
            "count": count,
            "limit": limit,
            "type": kind,
            "sort": sort,
        }

        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if category is not None:
            params["category"] = category
        if show is not None:
            params["show"] = show

        res = self.get(url, params=params)
        res.raise_for_status()

        res_json = res.json()

        return RedditListing.model_validate(res_json)

    def subreddits(
        self,
        subreddit: str,
        query: str,
        after: str | None = None,
        before: str | None = None,
        limit: int = 25,
        show: Literal["all"] | None = None,
    ):
        if len(query) > 512:
            raise ValueError("Query too long, max 512 characters.")
        if limit > 100:
            raise ValueError("Limit too high, max 100.")

        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {
            "q": query,
            "limit": limit,
        }

        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if show is not None:
            params["show"] = show

        return self.get(url, params=params)

    def get_post(self, permalink: str) -> dict:
        url = f"https://www.reddit.com{permalink}.json"
        res = self.get(url)
        res.raise_for_status()
        return res.json()
