from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel, Field
import models
from database import engine , SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from routers import auth
from models import Todo
from .auth import get_current_user
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
    prefix="/admin",
    tags=["admin"]
)

@router.get("/todo",status_code=status.HTTP_200_OK)
def read_all(user:user_dependencies,db:dependencies):
    if user is None or user["role"]!="admin":
        raise HTTPException(status_code=404, detail="Authentification error")
    
    else:
        todos = db.query(Todo).all()
        return todos
    
@router.delete("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def delete(user:user_dependencies,todo_id: int, db:dependencies):
    if user is None or user["role"]!="admin":
        raise HTTPException(status_code=404, detail="Authentification error")
    else:
        todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.get("id")).first()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        else:
            db.delete(todo)
            db.commit()
            return todo
    
