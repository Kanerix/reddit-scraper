from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


class RedditListing(BaseModel):
    kind: Literal["Listing"]
    data: RedditListingData


class ChildT1(BaseModel):
    kind: Literal["t1"]
    data: DataT1


class ChildT2(BaseModel):
    kind: Literal["t2"]
    data: DataT2


class ChildT3(BaseModel):
    kind: Literal["t3"]
    data: DataT3


class ChildT4(BaseModel):
    kind: Literal["t4"]
    data: DataT3


class ChildT5(BaseModel):
    kind: Literal["t5"]
    data: DataT3


class ChildT6(BaseModel):
    kind: Literal["t6"]
    data: DataT3


class ChildMore(BaseModel):
    kind: Literal["more"]
    data: DataMore


class DataT1(BaseModel):
    """Reddit Comment kind."""

    id: str
    name: str

    body: str
    link_id: str
    parent_id: str
    depth: int
    replies: RedditListing | None

    author: str

    subreddit: str
    subreddit_id: str

    score: int

    created: Annotated[datetime, datetime.fromtimestamp]

    @field_validator("replies", mode="before")
    @classmethod
    def validate_replies(cls, value: RedditListing | str):
        if isinstance(value, str):
            return None
        return value


class DataT2(BaseModel):
    """Reddit Account kind."""

    id: str


class DataT3(BaseModel):
    """Reddit Link (post) kind."""

    id: str
    name: str
    permalink: str

    title: str
    selftext: str
    thumbnail: str
    num_comments: int

    author: str

    subreddit: str
    subreddit_id: str
    subreddit_subscribers: int

    score: int
    upvote_ratio: float

    created: Annotated[datetime, datetime.fromtimestamp]


class DataT4(BaseModel):
    """Reddit Message kind."""

    id: str


class DataT5(BaseModel):
    """Reddit Subreddit kind."""

    id: str


class DataT6(BaseModel):
    """Reddit Award kind."""

    id: str


class DataMore(BaseModel):
    """Reddit More kind."""

    id: str
    name: str
    parent_id: str

    count: int
    depth: int

    children: list[str]


RedditChild = Annotated[
    ChildT1
    | ChildT2
    | ChildT3
    | ChildT4
    | ChildT5
    | ChildT6
    | ChildMore,
    Field(discriminator="kind"),
]


class RedditListingData(BaseModel):
    modhash: str
    # Used for pagination
    after: str | None
    before: str | None
    # The actual data
    children: list[RedditChild]
