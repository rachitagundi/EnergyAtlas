from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

Topic = Literal["Electricity", "Renewables", "Energy system"]
Kind = Literal["Data portal", "Overview", "Statistics"]


class SourceCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=3, max_length=200)
    publisher: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    url: HttpUrl = Field(max_length=2000)
    topic: Topic
    kind: Kind


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    publisher: str
    description: str
    url: str
    topic: Topic
    kind: Kind
    saved: bool


class BookmarkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    saved: bool = Field(strict=True)


class Overview(BaseModel):
    sources: int
    saved: int
    publishers: int
    database: str
