from pathlib import Path
from fastapi import Depends, APIRouter, HTTPException , Request , status
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
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates= Jinja2Templates(directory=str(Path(__file__).parent / "../templates"))



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
 
 
def redirect_to_login():
    redirect_response= RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
 
## Pages ###
@router.get("/todo-page/")
def render_todo_page(request : Request , db:dependencies):
    try :
        user= get_current_user(request.cookies.get('access_token'))
         
        if user is None:
            return redirect_to_login()
        todos= db.query(Todo).filter(Todo.owner_id==user.get("id"))
        
        return templates.TemplateResponse("todo.html" , {"request":request, "todos": todos, "user":user})
    except:
        return redirect_to_login()
    

@router.get("/add-todo-page")
def render_todo_page(request :Request):
    try:
        user =get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html",{"request":request,"user":user})
    
    except:
        return redirect_to_login()
    
@router.get("/edit-todo-page/{todo_id}")
def render_edit_todo_page(request: Request, todo_id: int, db: dependencies):
    try:
        user =  get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    except:
        return redirect_to_login()
            
        
        


#endPoint   
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
    
    todo_to_delete = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id==user.get("id")).first()
    
    if todo_to_delete is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_to_delete)
        db.commit()
        return {"message": "Todo deleted successfully"}