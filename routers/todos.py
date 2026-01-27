from fastapi import APIRouter, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from routers.auth import get_current_user, get_user_exceptions
from routers import auth


router=APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404:{"description":"Not Found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Todos(BaseModel):
    title:str
    description:Optional[str]=Field(None)
    priority:int = Field(gt=0,lt=6)
    complete:bool


@router.get("/")
async def read_all(db: Session=Depends(get_db)):
    return db.query(models.Todos).all()

@router.get("/user")
async def read_all_by_user(user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        return get_user_exceptions()
    data=db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
    return data


@router.get("/{todo_id}")
async def read_todo(todo_id:int, user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_item=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_item is not None:
        return todo_item
    raise http_exception()


@router.post("/")
async def create_todo(todo:Todos, user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_item=models.Todos(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
        owner_id=user.get("id")
    )
    db.add(todo_item)
    db.commit()
    return {
        'status_code':201,
        'data':db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
    }

@router.put("/{todo_id}")
async def update_todo(todo_id:int, todo:Todos, user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_item=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_item is None:
        raise http_exception()
    todo_item.title=todo.title
    todo_item.description=todo.description
    todo_item.priority=todo.priority
    todo_item.complete=todo.complete
    db.add(todo_item)
    db.commit()
    return {
        'status_code':200,
        'data':db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
    }

@router.delete("/{todo_id}")
async def delete_todo(todo_id:int, user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_item=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_item is None:
        raise http_exception()
    db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).delete()
    db.commit()
    return {
        'status_code':200,
        'data':db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo item not found")
