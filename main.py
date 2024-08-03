from fastapi import FastAPI
from utils import PostingsDatabase
from models import Posting, Poster
from typing import Any


app: FastAPI = FastAPI()
db: PostingsDatabase = PostingsDatabase()

my_id = 1


@app.get("/")
@app.get("/postings")
def show_postings() -> list[dict[str, Any]]:
    return db.get_all_postings()


@app.get("/postings/{id}")
def show_posting(id: int) -> dict[str, Any]:
    return db.get_posting(id)


@app.get("/mypostings")
def show_my_postings() -> list[dict[str, Any]]:
    return db.get_author_postings(my_id)


@app.post("/mypostings")
def add_posting(new_posting: Posting):
    return db.add_posting(new_posting)


@app.put("/mypostings/{id}")
def update_posting(id: int, new_posting: Posting):
    return db.update_posting(id, new_posting)
