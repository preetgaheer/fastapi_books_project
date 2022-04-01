from fastapi import FastAPI
from enum import Enum
from typing import Optional


app = FastAPI()

books = {'book_1' : { 'name': 'Wonders of World', 'author': 'William', 'rating': 55},
'book_2' : {'name': 'This is a book', 'author': 'James', 'rating': 23},
'book_3' : {'name': 'Web course', 'author': 'Shane', 'rating': 73},
'book_4' : {'name': 'All about sports', '': 'Daren', 'rating': 85},
}

class Directions(str, Enum):
    north= 'North'
    south= 'South'
    east = 'East'
    west='West'

@app.get('/books')
async def read_all_books():
    return books


@app.get('/directions/{direction_name}')
async def read_book_by_id(direction_name: Directions):
    if direction_name==Directions.north:
     return 'this is north'
    if direction_name==Directions.south:
     return 'this is south'
    if direction_name==Directions.east:
     return 'this is east'
    if direction_name==Directions.west:
     return 'this is west'

@app.post('/books')
async def add_new_book(book_name: str, author: str, rating: Optional[int] = 0):
    current_book_id = 0
    if len(books) > 0:
        for book in books:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    books[f'book_{current_book_id + 1}'] = {'name': book_name, 'author': author, 'rating' : rating}
    return books[f'book_{current_book_id + 1}']


@app.put("/{book_id}")
async def update_book(book_id: str, book_title: str, book_author: str, rating: int):
    book_information = {'name': book_title, 'author': book_author, 'rating': rating}
    books[f'book_{book_id}'] = book_information
    return book_information


@app.delete("/{book_id}")
async def delete_book(book_id):
    del books[f'book_{book_id}']
    return f'Book {book_id} deleted.'
