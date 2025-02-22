from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Literal


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
    data: (
        RedditChildrenT1
        | RedditChildrenT2
        | RedditChildrenT3
        | RedditChildrenT4
        | RedditChildrenT5
        | RedditChildrenT6
    )


class RedditChildrenT1(BaseModel):
    """Reddit Comment kind."""

    id: str
    title: str
    author: str
    body: str
    created: datetime
    replies: list[RedditListing]
    ups: int
    down: int
    score: int


class RedditChildrenT2(BaseModel):
    """Reddit Account kind."""

    id: str


class RedditChildrenT3(BaseModel):
    """Reddit Link (post) kind."""

    id: str
    permalink: str
    title: str
    selftext: str
    ups: int
    down: int
    score: int
    category: str | None


class RedditChildrenT4(BaseModel):
    """Reddit Message kind."""

    id: str


class RedditChildrenT5(BaseModel):
    """Reddit Subreddit kind."""

    id: str


class RedditChildrenT6(BaseModel):
    """Reddit Award kind."""

    id: str
