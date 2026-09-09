from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Library Management API")

# What information a book must have (Validation rules)
class Book(BaseModel):
    title: str
    author: str
    isbn: str
    available: bool = True

# In-memory database storing our library books
library_db = {
    1: {"title": "The Hobbit", "author": "J.R.R. Tolkien", "isbn": "978-0261102217", "available": True},
    2: {"title": "1984", "author": "George Orwell", "isbn": "978-0451524935", "available": False}
}

# 1. GET: Fetch all books in the library
@app.get("/books")
def get_all_books():
    return library_db

# 2. GET: Find a specific book using its ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in library_db:
        raise HTTPException(status_code=404, detail="Book not found in library")
    return library_db[book_id]

# 3. POST: Add a brand new book to the library
@app.post("/books")
def add_book(book: Book):
    new_id = max(library_db.keys()) + 1 if library_db else 1
    library_db[new_id] = book.model_dump()
    return {"id": new_id, **library_db[new_id]}

# 4. PUT: Update a book's details (e.g., changing availability or title)
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in library_db:
        raise HTTPException(status_code=404, detail="Book not found")
    library_db[book_id] = book.model_dump()
    return {"message": "Book updated successfully", "book": library_db[book_id]}

# 5. DELETE: Remove a book from the library system
@app.delete("/books/{book_id}")
def remove_book(book_id: int):
    if book_id not in library_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del library_db[book_id]
    return {"message": "Book successfully removed from library"}
