from fastapi import FastAPI

app=FastAPI()


BOOKS = {
    "book_1": {"title": "The Alchemist", "author": "Paulo Coelho"},
    "book_2": {"title": "1984", "author": "George Orwell"},
    "book_3": {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    "book_4": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book_5": {"title": "Pride and Prejudice", "author": "Jane Austen"}
}


@app.get("/")
async def read_books():
    return BOOKS

@app.post("/")
async def create_book(title,author):
    book_id=f"book_{len(BOOKS)+1}"
    BOOKS[book_id]={'title':title,'author':author}
    return BOOKS

@app.put('/{book_id}')
async def update_book(book_id:str, title:str, author:str):
    book_info={'title':title,'author':author}
    for key in BOOKS.keys():
        if(key==book_id):
            BOOKS[key]=book_info
            return BOOKS
    return {"error":"Book not found"}

@app.delete('/{book_id}')
async def delete_book(book_id:str):
    if book_id in BOOKS:
        del BOOKS[book_id]
        return BOOKS
    return {"error":"Book not found"}
