from fastapi import APIRouter, Body , HTTPException
from fastapi.encoders import jsonable_encoder


from server.database import (
    add_book,
    delete_book,
    retrieve_books,
    retrieve_book,
    update_book,
)
from server.models.book import (
    ResponseModel,
    BookSchema,
    UpdateBookModel,
)

router = APIRouter()

@router.get("/", response_description="Books retrieved")
async def get_books():
    books = await retrieve_books()
    if books:
        return ResponseModel(books, "Books data retrieved successfully")
    else:
        raise HTTPException(status_code=404, detail={'error': 'Failed to read books'})
        

@router.post("/", response_description="Book data added into the database")
async def add_book_data(book: BookSchema = Body(...)):
    if book:
        book = jsonable_encoder(book)
        new_book = await add_book(book)
        return ResponseModel(new_book, "Book added successfully.")
    else:
        raise HTTPException(status_code=404, detail={'error': 'Failed to add new book'})


@router.get("/{id}", response_description="Student data retrieved")
async def get_book_data(id):
    book = await retrieve_book(id)
    if book:
        return ResponseModel(book, "Book data retrieved successfully")
    else:
        raise HTTPException(status_code=404, detail={'error': 'Failed to fetch book'})


@router.put("/{id}")
async def update_book_data(id: int, req: UpdateBookModel):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_book = await update_book(id, req)
    print(updated_book)
    if updated_book:
        show_book = await retrieve_book(id)
        return ResponseModel(show_book, "Book name updated successfully")
    else:
        raise HTTPException(status_code=404, detail={'error': 'Book Not Found'})
    

@router.delete("/{id}", response_description="Book data deleted from the database" )
async def delete_book_data(id: int):
    deleted_book = await delete_book(id)
    if deleted_book:
        return f'Book deleted successfully'
    else:
        raise HTTPException(status_code= 404 , detail = {'error': f'book with id {id} not found '})
    