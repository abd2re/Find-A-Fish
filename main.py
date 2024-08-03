from fastapi import FastAPI
from utils import PostingsDatabase

app = FastAPI()

user_id = 1
postings_database: Po


@app.get("/")
@app.get("/postings")
def show_postings():
    return postings_database


@app.get("/postings/{id}")
def show_posting(id: int):
    posting: Posting = next(
        filter(lambda posting: posting["id"] == id, postings_database)
    )
    return posting


@app.get("/mypostings")
def show_my_postings():
    my_postings: list[Posting] = list(
        filter(lambda posting: posting["author_id"] == user_id, postings_database)
    )
    return my_postings


@app.post("/mypostings")
def create_posting(new_posting: Posting):
    new_posting_dict = new_posting.model_dump()
    new_posting_dict["id"] = randint(10000000, 99999999)
    postings_database.append(new_posting_dict)
    return new_posting_dict


@app.put("/mypostings/{id}")
def create_posting(id: int, new_posting: Posting):
    try:
        old_posting: Posting = next(
            filter(lambda posting: posting["id"] == id, postings_database)
        )
    except StopIteration:
        raise HTTPException(status_code=404, detail="Post not found")

    postings_database.remove(old_posting)

    new_posting_dict = new_posting.model_dump()
    new_posting_dict["id"] = id
    postings_database.append(new_posting_dict)

    return new_posting_dict
