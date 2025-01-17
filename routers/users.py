from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel, Field
import models
from database import engine , SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from routers import auth
from models import Todo , Users
from .auth import get_current_user
from passlib.context import CryptContext


bcrypt=CryptContext(schemes=['bcrypt'], deprecated='auto')
router=APIRouter()
models.Base.metadata.create_all(bind=engine) 
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
dependencies = Annotated[Session, Depends(get_db)]
user_dependencies = Annotated[Session, Depends(get_current_user)]

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/todo",status_code=status.HTTP_200_OK)
def get_user(user:user_dependencies,db:dependencies):
    if user is None :
        raise HTTPException(status_code=404, detail="Authentification error")
    
    else:
        todos = db.query(Users).filter(Users.id == user["id"]).all()
        return todos
    
    
class changePass(BaseModel):
    password: str = Field(min_length=1)
    new_password: str = Field(min_length=6)
    
@router.put("/change_password",status_code=status.HTTP_200_OK)
def change_password(user:user_dependencies,change:changePass,db:dependencies):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentification error")
    
    else:
        user = db.query(Users).filter(Users.id == user["id"]).first()
        if bcrypt.verify(change.password,user.hashed_password):
            user.hashed_password=bcrypt.hash(change.new_password)
            db.commit()
            db.refresh(user)
            return user
        else:
            raise HTTPException(status_code=404, detail="Password incorrect")