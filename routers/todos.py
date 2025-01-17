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
router=APIRouter(
    prefix="/todos",
    tags=["todos"]
)
models.Base.metadata.create_all(bind=engine) 
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
dependencies = Annotated[Session, Depends(get_db)]
user_dependencies = Annotated[Session, Depends(get_current_user)]

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str= Field(min_length=1, max_length=100)
    priority: int= Field(ge=1, le=5)
    complete: bool
    
@router.get("/",status_code=status.HTTP_200_OK)
def read_all(user:user_dependencies,db:dependencies):
    #voir cest quoi dependency injection
    todos = db.query(Todo).filter(Todo.owner_id == user["id"]).all()
    return todos

@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
def read_one(user:user_dependencies,todo_id: int, db:dependencies):
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user["id"]).all()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        return todo
    
@router.post("/todos/",status_code=status.HTTP_201_CREATED)
def create(user:user_dependencies,todo: TodoCreate, db:dependencies):
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_todo= Todo(**todo.dict(),owner_id=user["id"])
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/todos/{todo_id}",status_code=status.HTTP_200_OK)
def update(user:user_dependencies,todo_id: int, todo: TodoCreate, db:dependencies):
    todo_to_update = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.get("id")).first()
    if todo_to_update is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        for key, value in todo.dict().items():
            setattr(todo_to_update, key, value)
        db.commit()
        db.refresh(todo_to_update)
        return todo_to_update

@router.delete("/todos/{todo_id}",status_code=status.HTTP_200_OK)
def delete(user:user_dependencies,todo_id: int, db:dependencies):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentification failed")
    
    todo_to_delete = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.id).first()
    
    if todo_to_delete is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_to_delete)
        db.commit()
        return {"message": "Todo deleted successfully"}