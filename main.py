from fastapi import FastApi
from pydantic import BaseModel

app = FastApi()


@app.get("/")
def root():
    return {"Hello": "World"}
