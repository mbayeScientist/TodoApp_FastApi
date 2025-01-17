from fastapi import Depends, FastAPI, HTTPException, Request
from . import models
from database import engine
from routers import auth, todos, admin ,users

from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="TODOAPP/templates")
@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

models.Base.metadata.create_all(bind=engine) 
app.include_router(auth.router)  
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# dependencies = Annotated[Session, Depends(get_db)]

# class TodoCreate(BaseModel):
#     title: str = Field(min_length=1, max_length=100)
#     description: str= Field(min_length=1, max_length=100)
#     priority: int= Field(ge=1, le=5)
#     complete: bool
    
# @app.get("/",status_code=status.HTTP_200_OK)
# def read_all(db:dependencies):
#     #voir cest quoi dependency injection
#     todos = db.query(Todo).all()
#     return todos

# @app.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
# def read_one(todo_id: int, db:dependencies):
#     todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if todo is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     else:
#         return todo
    
# @app.post("/todos/",status_code=status.HTTP_201_CREATED)
# def create(todo: TodoCreate, db:dependencies):
#     new_todo= Todo(**todo.dict())
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return new_todo

# @app.put("/todos/{todo_id}",status_code=status.HTTP_200_OK)
# def update(todo_id: int, todo: TodoCreate, db:dependencies):
#     todo_to_update = db.query(Todo).filter(Todo.id == todo_id).first()
#     if todo_to_update is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     else:
#         for key, value in todo.dict().items():
#             setattr(todo_to_update, key, value)
#         db.commit()
#         db.refresh(todo_to_update)
#         return todo_to_update

# @app.delete("/todos/{todo_id}",status_code=status.HTTP_200_OK)
# def delete(todo_id: int, db:dependencies):
#     todo_to_delete = db.query(Todo).filter(Todo.id == todo_id).first()
#     if todo_to_delete is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     else:
#         db.delete(todo_to_delete)
#         db.commit()
#         return {"message": "Todo deleted successfully"}