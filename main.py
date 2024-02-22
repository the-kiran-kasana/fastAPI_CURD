from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    pages: int

# Dummy data
books_db = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling", "year": 1997, "pages": 332},
    {"id": 2, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "pages": 310},
]

@app.get("/books/", response_model=List[Book])
async def get_books():
    return books_db

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    books_db.append(book.dict())
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    for b in books_db:
        if b["id"] == book_id:
            b.update(book.dict())
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[i]
            return book
    raise HTTPException(status_code=404, detail="Book not found")
