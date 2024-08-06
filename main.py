from fastapi import FastAPI, Query, HTTPException
from utils import PostingsDatabase, PostingObject, PosterDatabase
from models import PostingModel, PosterModel
from typing import Any, Annotated


app: FastAPI = FastAPI()
postings_db: PostingsDatabase = PostingsDatabase()
posters_db: PosterDatabase = PosterDatabase()


## All postings
@app.get("/")
@app.get("/home")
def get_all_postings():
    return postings_db.get_all_postings()


# Operate on a posting


@app.get("/post")
def get_posting(id: int):
    return postings_db.get_posting(id)


@app.post("/post")
def add_posting(new_posting: PostingModel):
    if postings_db.ValidatePosting.author(new_posting, posters_db):
        return postings_db.add_posting(new_posting)
    else:
        raise HTTPException(status_code=404, detail="Author id doesn't exist")


@app.put("/post")
def update_posting(id: int, new_posting: PostingModel):
    if postings_db.ValidatePosting.author(new_posting, posters_db):
        return postings_db.update_posting(id, new_posting)
    else:
        raise HTTPException(status_code=404, detail="Author id doesn't exist")


@app.delete("/post")
def delete_posting(id: int):
    return postings_db.delete_posting(id)


## All posters
@app.get("/posters")
def get_all_posters():
    return posters_db.get_all_posters()


## Get poster's history
@app.get("/posters/{username}")
@app.get("/@{username}")
def get_poster_postings(username: str):
    poster: PosterModel = posters_db.get_poster_by_name(username)
    return postings_db.get_author_postings(poster.id)


## Utility functions, not to be used in production


@app.post("/posters")
def add_poster(new: Annotated[str, Query(pattern="^[A-Za-z0-9_]{4,15}$")]):
    return posters_db.add_poster(new)


@app.post("/postmany")
def add_posting(postings: list[PostingModel]):
    for new_posting in postings:
        postings_db.add_posting(new_posting)
