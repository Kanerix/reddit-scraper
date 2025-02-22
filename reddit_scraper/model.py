from __future__ import annotations
from typing_extensions import Literal

from pydantic import BaseModel


class RedditListing(BaseModel):
    kind: Literal["Listing"]
    data: RedditListingData


class RedditListingData(BaseModel):
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


class RedditChildrenT1(BaseModel):
    """Reddit Comment kind."""
    title: str
    author: str
    body: str
    created: str
    replies: list[RedditListing]
    ups: int
    down:int
    score: int
    total_awards_received: str

class RedditChildrenT2(BaseModel):
    """Reddit Account kind."""

class RedditChildrenT3(BaseModel):
    """Reddit Link (post) kind."""
    permalink: str
    title: str
    selftext: str
    ups: int
    down:int
    score: int
    category: str | None


class RedditChildrenT4(BaseModel):
    """Reddit Message kind."""

class RedditChildrenT5(BaseModel):
    """Reddit Subreddit kind."""

class RedditChildrenT6(BaseModel):
    """Reddit Award kind."""