from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from typing_extensions import Literal


class RedditListing(BaseModel):
    kind: Literal["Listing"]
    data: RedditListingData


class ChildrenT1(BaseModel):
    kind: Literal["t1"]
    data: DataT1


class ChildrenT2(BaseModel):
    kind: Literal["t2"]
    data: DataT2


class ChildrenT3(BaseModel):
    kind: Literal["t3"]
    data: DataT3


class ChildrenT4(BaseModel):
    kind: Literal["t4"]
    data: DataT3


class ChildrenT5(BaseModel):
    kind: Literal["t5"]
    data: DataT3


class ChildrenT6(BaseModel):
    kind: Literal["t6"]
    data: DataT3


class ChildrenMore(BaseModel):
    kind: Literal["more"]
    data: DataMore


class DataT1(BaseModel):
    """Reddit Comment kind."""

    id: str

    subreddit: str
    subreddit_id: str
    title: str
    author: str
    body: str
    created: datetime
    replies: list[RedditListing]


class DataT2(BaseModel):
    """Reddit Account kind."""

    id: str


class DataT3(BaseModel):
    """Reddit Link (post) kind."""

    id: str
    permalink: str

    title: str
    author: str
    num_comments: int

    subreddit: str
    subreddit_id: str
    subreddit_subscribers: int

    score: int
    ups: int
    downs: int

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
    count: int
    name: str
    parent_id: str
    depth: int
    children: list[str]


RedditChildren = Annotated[
    ChildrenT1 | ChildrenT2 | ChildrenT3 | ChildrenT4 | ChildrenT5 | ChildrenT6 | ChildrenMore, Field(discriminator="kind")
]


class RedditListingData(BaseModel):
    modhash: str
    # Used for pagination
    after: str | None
    before: str | None
    # The actual data
    children: list[RedditChildren]
