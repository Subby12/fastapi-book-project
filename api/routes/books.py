from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()
db = InMemoryDB()

# Initialize with sample books
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,  # Changed from FANTASY to SCI_FI
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

@router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_books():
    books = list(db.get_books().values())
    return [book for book in books]  # Return list of Book objects

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> Book:
    book = db.get_book(book_id)
    if book is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"Book with id {book_id} not found"}
        )
    return book
