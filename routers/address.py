from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import Optional
from pydantic import BaseModel, Field


router=APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404:{"description":"Not found"}}
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Address(BaseModel):
    address1:str
    address2:Optional[str]=Field(None)
    city:str
    state:str
    country:str

@router.post("/")
async def create_address(address:Address, db:Session=Depends(get_db)):
    address_item=models.Address(
        address1=address.address1,
        address2=address.address2,
        city=address.city,
        state=address.state,
        country=address.country
    )
    db.add(address_item)
    db.commit()
    return {"message":"Address created successfully"}
