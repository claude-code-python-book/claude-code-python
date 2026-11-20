"""A model written for Pydantic 1, run on Pydantic 2."""

import warnings

import pydantic
from pydantic import BaseModel, validator

warnings.simplefilter("default")
print("pydantic", pydantic.VERSION)


class Book(BaseModel):
    title: str
    year: int

    class Config:
        orm_mode = True

    @validator("title")
    def strip_title(cls, value):
        return value.strip()


book = Book.parse_obj({"title": "  Fluent Python ", "year": "2022"})
print(book.dict())
