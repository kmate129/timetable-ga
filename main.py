"""
This is the main module of the application.
It contains the entry point and setup for the FastAPI app.
"""

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """GET endpoint that returns a simple JSON response."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """GET endpoint that returns the item_id and query parameter."""
    return {"item_id": item_id, "q": q}
