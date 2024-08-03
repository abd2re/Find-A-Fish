from pydantic import BaseModel


class Poster(BaseModel):
    user: str
    postings: list[int]


class Posting(BaseModel):
    author_id: int
    title: str
    embed: str
    industry: str
    skills: list[str]
    location: tuple[str | None, str | None] = "International", None
    remote: bool | None = True
