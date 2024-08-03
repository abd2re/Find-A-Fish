from models import Posting
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from random import randint


class PostingsDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostingsDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.postings = list()

    def __repr__(self) -> str:
        return f"PostingsDatabase({self.postings})"

    def find_posting(self, posting_id: int) -> Posting:
        try:
            return next(
                filter(lambda posting: posting["id"] == posting_id, self.postings)
            )
        except StopIteration:
            raise HTTPException(status_code=404, detail="Post not found")

    def get_author_postings(self, author_id: int) -> list[Posting]:
        try:
            return list(
                filter(lambda posting: posting["author_id"] == author_id, self.postings)
            )
        except KeyError:
            raise HTTPException(status_code=404, detail="User not found")

    def add_posting(self, posting: Posting) -> str:
        posting_dict: dict[str, Any] = posting.model_dump()
        new_id: int = randint(10000000, 99999999)
        posting_dict["id"] = new_id
        self.postings.append(posting_dict)

        return f"Posting with id {new_id} has been added."

    def update_posting(self, posting_id: int, new_posting: Posting) -> str:
        old_posting: Posting = self.find_posting(posting_id)
        new_posting_dict: dict[str, Any] = new_posting.model_dump()
        new_posting_dict["id"] = posting_id

        self.postings.remove(old_posting)
        self.postings.append(new_posting_dict)

        return f"Posting with id {posting_id} has been updated."
