from fastapi import APIRouter, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exceptions, verify_pass, get_hash_pass

router=APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404:{"description":"Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

class UserVerification(BaseModel):
    username:str
    password:str
    new_password:str


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
async def read_all_users(db:Session=Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/{user_id}")
async def user_by_path(user_id:int, db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if user is not None:
        return user
    return 'Invalid User'

@router.get("/user/")
async def user_by_query(user_id:int, db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if user is not None:
        return user
    return 'Invalid User'


@router.put("/change_password")
async def change_password(user_verification:UserVerification,
                          user:dict=Depends(get_current_user),
                          db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()

    user_db=db.query(models.Users).filter(models.Users.id==user.get("id")).first()

    if user_db is not None:
        if(user_db.username==user_verification.username and verify_pass(user_verification.password, user_db.hashed_password)):
            user_db.hashed_password=get_hash_pass(user_verification.new_password)
            db.add(user_db)
            db.commit()
            return 'Password updated successfully'

    return 'Invalid Request'


@router.delete("/delete_user")
async def delete_user(
                      user:dict=Depends(get_current_user),
                      db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()

    user_db=db.query(models.Users).filter(models.Users.id==user.get("id")).first()
    if user_db is not None:
        db.delete(user_db)
        db.commit()
        return 'User deleted successfully'
    return 'Invalid Request'
