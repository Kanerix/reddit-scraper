from __future__ import annotations

from pydantic import BaseModel


class RedditResponse(BaseModel):
    kind: str
    data: RedditResponseData


class RedditResponseData(BaseModel):

    # Used for pagination
    after: str | None
    before: str | None
    # The actual data
    children: list[RedditChildren]


class RedditChildren(BaseModel):
    kind: str
    permalink: str
    title: str
    author: str
    subreddit: str
    subreddit_subscribers: int
    num_comments: int
    ups: int
    downs: int
    score: int
    created: int


class RedditChildrenT3(BaseModel):
    """T3 is the type for posts."""
    permalink: str
    title: str
    selftext: str
    ups: int
    down:int
    score: int
    category: str | None


class RedditPostDataChildrenT1(BaseModel):
    """T1 is the type for comments."""
    title: str
    author: str
    body: str
    created: str
    replies: list[RedditPostDataChildrenT1]
    ups: int
    down:int
    score: int
    total_awards_received: str