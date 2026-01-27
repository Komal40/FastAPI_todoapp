from fastapi import FastAPI, HTTPException, Request, status, Form
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse

class NegativeNumberException(Exception):
    def __init__(self, books_to_return:int):
        self.book_to_return=books_to_return


app = FastAPI()

BOOKS=[]

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exc:NegativeNumberException):
    return JSONResponse(status_code=400,
                         content={ "message":f"Invalid number of books to return: {exc.book_to_return}. Must be a positive integer."})

class Book(BaseModel):
    id:UUID
    title: str = Field(min_length=1)
    author:str
    desc: Optional[str] = Field(title="Description of the book",
                    #  default=None,
                     min_length=1,
                     max_length=100)
    rating:int

class BookNoRating(BaseModel):
    id:UUID
    title:str = Field(min_length=1)
    author:str

@app.get("/book/login")
async def book_login(username:str=Form(...), password:str=Form(...)):
    return {"username":username, "password":password}


@app.get("/")
async def read_books(book_to_return:Optional[int]=None):
    if(book_to_return and book_to_return<0):
        raise NegativeNumberException(books_to_return=book_to_return)
    if(len(BOOKS)<1):
        create_initial_books()
    if(book_to_return and book_to_return>0):
        return BOOKS[0:book_to_return]
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    BOOKS.append(book)
    return BOOKS


@app.get("/book/{book_id}")
async def getBookById(book_id:str):
    for book in BOOKS:
        if(str(book.id)==book_id):
            return book
    raise raise_item_cannot_found()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def getBookByIdNoRating(book_id:str):
    for book in BOOKS:
        if(str(book.id)==book_id):
            return book
    raise raise_item_cannot_found()

@app.put("/update_book/{book_id}")
async def update_book(book_id:str, book:Book):
    for x in range(len(BOOKS)):
        if(str(BOOKS[x].id)==book_id):
            BOOKS[x]=book
            return BOOKS[x]
    raise raise_item_cannot_found()



@app.delete("/delete_book/{book_id}")
async def delete_book(book_id:str):
    for x in range(len(BOOKS)):
        if(str(BOOKS[x].id)==book_id):
            del BOOKS[x]
            return BOOKS
    raise raise_item_cannot_found()


def create_initial_books():
    book1=Book(
        id="123e4567-e89b-12d3-a456-426614174000",
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        desc="A novel set in the Roaring Twenties.",
        rating=5)
    book2=Book(
        id="113e4567-e89b-12d3-a456-426614174000",
        title="The Great ",
        author="Fitzgerald",
        desc="A novel",
        rating=5)
    BOOKS.extend([book1,book2])


def raise_item_cannot_found():
    return HTTPException(status_code=404,
                         detail="Book with the given ID not found.",
                         headers={"X-Header_Error":"Book not found"})
