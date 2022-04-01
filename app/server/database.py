import motor.motor_asyncio
from bson.objectid import ObjectId

from fastapi import APIRouter, Body , HTTPException
from mysqlx import InternalError

MONGO_DETAILS = "mongodb+srv://preetgaheer:10119713@cluster0.zl9cz.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.books

books_collection = database.get_collection("books")



def book_helper(book) -> dict:
    return {
        "object_id": str(book["_id"]),
        'id': int(book['id']),
        "title": str(book["title"]),
        "author": str(book["author"]),
        'description' :str(book['description']),
        "rating": int(book["rating"]),
    }

# Retrieve all books present in the database
async def retrieve_books():
    books = []
    async for book in books_collection.find():
        books.append(book_helper(book))
    return books


# Add a new book into to the database
async def add_book(book_data: dict) -> dict:
    book = await books_collection.insert_one(book_data)
    new_book = await books_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)


# Retrieve a book with a matching ID
async def retrieve_book(id: int) -> dict:
    book = await books_collection.find_one({'id': int(id)})
    if book:
        return book_helper(book)


# Update a book with a matching ID
async def update_book(id: int, data: dict):
    # Return false if an empty request body is sent.
    try:
        book = await books_collection.find_one({'id': int(id)})
        if book:
            updated_book = await books_collection.update_one({'id': int(id)} ,{"$set": data})
            if updated_book:
                print('hehe')
                return updated_book
        else:
            raise HTTPException(status_code= 404 , detail='Please enter valid data')
    except:
        raise HTTPException(status_code=500, detail=f'Failed Fetching from db')
        

# Delete a book from the database
async def delete_book(id: str):
    book = await books_collection.find_one({'id': int(id)})
    if book:
        await books_collection.delete_one({'id': int(id)})
        return True