from __future__ import annotations
from models import Posting
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from random import randint


class PostingsDatabase:
    _instance: PostingsDatabase = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostingsDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized: bool = True
            self.__postings: list = list()

    def __repr__(self) -> str:
        return f"PostingsDatabase({self.__postings})"

    def get_all_postings(self) -> list[dict[str, Any]]:
        return self.__postings

    def get_posting(self, posting_id: int) -> dict[str, Any]:
        try:
            return next(
                filter(lambda posting: posting["id"] == posting_id, self.__postings)
            )
        except StopIteration:
            raise HTTPException(status_code=404, detail="Post not found")

    def get_author_postings(self, author_id: int) -> list[dict[str, Any]]:
        return list(
            filter(lambda posting: posting["author_id"] == author_id, self.__postings)
        )

    @staticmethod
    def add_id(id: int, posting: Posting) -> dict[str, Any]:
        posting_dict: dict[str, Any] = posting.model_dump()
        posting_dict["id"] = id
        return posting_dict

    def add_posting(self, posting: Posting) -> str:
        new_id: int = randint(10000000, 99999999)
        posting: dict[str, Any] = self.add_id(new_id, posting)
        self.__postings.append(posting)

        return f"Posting with id {new_id} has been added."

    def update_posting(self, posting_id: int, new_posting: Posting) -> str:
        old_posting: Posting = self.get_posting(posting_id)
        new_posting: dict[str, Any] = self.add_id(posting_id, new_posting)
        self.__postings.remove(old_posting)
        self.__postings.append(new_posting)

        return f"Posting with id {posting_id} has been updated."
