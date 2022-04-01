from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
# from uuid import UUID
from typing import Optional

app = FastAPI()

books = []

class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

class Book(BaseModel):
    id: int = Field(gt=-1)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=50,
                                       min_length=1, default='No Description')
    rating: Optional[int] = Field(gt=-1, lt=101, default=0) 

    class Config:
        schema_extra = {
            "example": {
                "id": "9",
                "title": "Professional editor",
                "author": "Bonnac",
                "description": "This is the description",
                "rating": 90
            }
        }

def create_books_no_api():
    book_1 = Book(id="1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=40)
    book_2 = Book(id="2",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=81)
    book_3 = Book(id="3",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=66)
    book_4 = Book(id="4",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=53)
    books.append(book_1)
    books.append(book_2)
    books.append(book_3)
    books.append(book_4)

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Cant read {exception.books_to_return} "
                            f"books? You need to read more!"}
    )

def item_not_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header_Error":
                                  "No matching UUID "})

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(books) < 1:
        create_books_no_api()

    if books_to_return and len(books) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(books[i - 1])
            i += 1
        return new_books
    return books

@app.get("/book/{book_id}")
async def read_book(book_id: Book.id):
    for x in books:
        if x.id == book_id:
            return x
    raise item_not_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    books.append(book)
    return book

@app.put("books/{book_id}")
async def update_book(book_id: Book.id, book: Book):
    counter = 0

    for x in books:
        counter += 1
        if x.id == book_id:
            books[counter - 1] = book
            return books[counter - 1]
    raise item_not_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: Book.id):
    counter = 0

    for x in books:
        counter += 1
        if x.id == book_id:
            del books[counter - 1]
            return f'Book with ID:{book_id} is deleted'
    raise item_not_found_exception()

