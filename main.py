from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import models
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permet toutes les origines (vous pouvez spécifier des URLs spécifiques ici)
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


