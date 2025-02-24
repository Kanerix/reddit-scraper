from typing import Literal, override

from httpx import Client

from scrp.agents import get_agent
from scrp.model import RedditListing


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
        if res.status_code == 429:
            raise RateLimitError(res.status_code, res.headers.get("x-ratelimit-reset"))

        res.raise_for_status()

        return RedditListing.model_validate(res.json())

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
        params: dict[str, str | int | float] = {
            "q": query,
            "limit": limit,
        }

        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if show is not None:
            params["show"] = show

        res = self.get(url, params=params)
        if res.status_code == 429:
            raise RateLimitError(res.status_code, res.headers.get("x-ratelimit-reset"))

        res.raise_for_status()

        return RedditListing.model_validate(res.json())

    def comments(
        self,
        permalink: str,
        comment: int | None = None,
        depth: int | None = None,
        limit: int | None = None,
        showedits: bool = False,
        showmedia: bool = False,
        showmore: bool = False,
        threaded: bool = False,
        sort: Literal[
            "confidence", "top", "new", "controversial", "old", "random", "qa"
        ] = "confidence",
        theme: Literal["light", "dark"] = "dark",
    ) -> list[RedditListing]:
        url = f"https://www.reddit.com{permalink}.json"
        params: dict[str, str | int | float] = {
            "theme": theme,
            "sort": sort,
        }

        if comment is not None:
            params["comment"] = comment
        if depth is not None:
            params["depth"] = depth
        if limit is not None:
            params["limit"] = limit
        if showedits:
            params["showedits"] = "yes"
        if showmedia:
            params["showmedia"] = "yes"
        if showmore:
            params["showmore"] = "yes"
        if threaded:
            params["threaded"] = "yes"

        res = self.get(url, params=params)
        if res.status_code == 429:
            raise RateLimitError(res.status_code, res.headers.get("x-ratelimit-reset"))

        res.raise_for_status()

        comments: list[RedditListing] = list(
            map(RedditListing.model_validate, res.json())
        )

        return comments


class RateLimitError(Exception):
    def __init__(self, status_code: int, retry_after: str | None):
        self.status_code = status_code
        self.retry_after = int(retry_after) if retry_after else None
        super().__init__(f"Rate limit exceeded, retry after {retry_after} seconds.")
