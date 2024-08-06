from pydantic import BaseModel
from datetime import datetime


class PosterModel(BaseModel):
    id: int
    username: str


class PostingModel(BaseModel):
    author_id: int
    title: str
    embed: str
    date_time: datetime | None = datetime.now()
    skills: list[str]
    location: tuple[str | None, str | None] = "International", None
    remote: bool | None = True
