from fastapi import Depends, FastAPI, HTTPException, Request, status
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth, todos, admin ,users
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
app = FastAPI()


app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse("/todos/todo-page" ,status_code=status.HTTP_302_FOUND )

models.Base.metadata.create_all(bind=engine) 
app.include_router(auth.router)  
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

app.add_middleware(HTTPSRedirectMiddleware)


