from __future__ import annotations
from models import Posting, Poster
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from random import randint

PostingObject = dict[str, Any]


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

    def get_all_postings(self) -> list[PostingObject]:
        return self.__postings

    def get_posting(self, posting_id: int) -> PostingObject:
        try:
            return next(
                filter(lambda posting: posting["id"] == posting_id, self.__postings)
            )
        except StopIteration:
            raise HTTPException(
                status_code=404, detail=f"Posting with id {posting_id} not found"
            )

    def get_author_postings(self, author_id: int) -> list[PostingObject]:
        return list(
            filter(lambda posting: posting["author_id"] == author_id, self.__postings)
        )

    def add_posting(self, posting: Posting) -> str:
        new_id: int = randint(10000000, 99999999)
        posting: PostingObject = self.add_id(new_id, posting)
        self.__postings.append(posting)

        return f"Posting with id {new_id} has been added."

    def update_posting(self, posting_id: int, new_posting: Posting) -> str:
        old_posting: Posting = self.get_posting(posting_id)
        new_posting: PostingObject = self.add_id(posting_id, new_posting)
        self.__postings.remove(old_posting)
        self.__postings.append(new_posting)

        return f"Posting with id {posting_id} has been updated."

    def delete_posting(self, posting_id: int) -> str:
        posting: Posting = self.get_posting(posting_id)
        self.__postings.remove(posting)

        return f"Posting with id {posting_id} has been deleted."

    @staticmethod
    def add_id(id: int, posting: Posting) -> PostingObject:
        posting_dict: PostingObject = posting.model_dump()
        posting_dict["id"] = id
        return posting_dict

    class ValidatePosting:

        @staticmethod
        def author(posting: Posting, poster_database: PosterDatabase) -> bool:
            author_id = posting.author_id
            if poster_database.get_poster_by_id(author_id):
                return True
            return False


class PosterDatabase:
    _instance: PosterDatabase = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PosterDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized: bool = True
        self.__posters: list[Poster] = list()

    def get_all_posters(self) -> list[Poster]:
        return self.__posters

    def add_poster(self, username: str) -> str:
        new_id: int = randint(10000000, 99999999)
        self.__posters.append(
            Poster.model_validate({"id": new_id, "username": username})
        )

        return f"Poster with id {new_id} has been added."

    def get_poster_by_id(self, poster_id: int) -> Poster:
        try:
            return next(filter(lambda poster: poster.id == poster_id, self.__posters))
        except StopIteration:
            raise HTTPException(
                status_code=404, detail=f"Poster with id {poster_id} not found"
            )

    def get_poster_by_name(self, username: str) -> Poster:
        try:
            return next(
                filter(lambda poster: poster.username == username, self.__posters)
            )
        except StopIteration:
            raise HTTPException(
                status_code=404, detail=f"Poster with username {username} not found"
            )
