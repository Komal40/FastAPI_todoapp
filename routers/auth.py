# import sys
# sys.path.append("..")


from fastapi import Depends, HTTPException, status, APIRouter
import models
from pydantic import BaseModel, Field
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal,engine, get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES




class CreateUser(BaseModel):
    email:Optional[str]
    username:str
    first_name:str
    last_name:str
    password:str


models.Base.metadata.create_all(bind=engine)

oauth2Bearer=OAuth2PasswordBearer(tokenUrl="token")


router=APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user":"Not authenticate"}}
)



bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hash_pass(password):
    return bcrypt_context.hash(password)

def verify_pass(password, hash_pass):
    return bcrypt_context.verify(password, hash_pass)

def authenticate_user(username:str, password:str, db):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if user is None:
        return False
    if not verify_pass(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, expires_delta:Optional[timedelta]=None):
    encode={"sub":username,"id":user_id}
    if expires_delta:
        expire=datetime.utcnow() + expires_delta
    else:
        expire=datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp":expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token:str=Depends(oauth2Bearer)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        user_id:int=payload.get("id")
        if username is None or user_id is None:
            raise get_user_exceptions()
        return {"username":username, "id":user_id}
    except JWTError:
        raise get_user_exceptions()


@router.post("/create/user")
async def create_user(user:CreateUser, db:Session=Depends(get_db)):
    hash_pass=get_hash_pass(user.password)
    new_user=models.Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hash_pass,
        is_active=True
    )

    db.add(new_user)
    db.commit()

    return {
        'status_code':201,
        'data':db.query(models.Users).all()
    }


@router.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires=timedelta(minutes=30)
    token=create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"access_token":token, "token_type":"bearer"}




def get_user_exceptions():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate":"Bearer"}
    )
