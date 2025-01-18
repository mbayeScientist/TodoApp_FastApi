from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pathlib import Path
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import APIRouter , Depends , HTTPException , Request
from fastapi.templating import Jinja2Templates

SECRET_KEY= "8ed0aedc8e6e6aed1628c9427cc3976f019a86a59f3236267e7de7f7b28767e2"
ALGORITHM = "HS256"
#instance de CryptContext
bcrypt=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_beare=OAuth2PasswordBearer(tokenUrl="auth/token")   

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
dependencies = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory=str(Path(__file__).parent / "../templates"))


### Pagees###
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html" , {"request": request})

@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse("register.html" , {"request": request})


###templates
#classe pydantic pour la creation d'un utilisateur
class UserCreate(BaseModel):
    email: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)
    role: str = Field(min_length=1, max_length=100)
    is_active:  Optional[bool] = True
#creation d'une classe toekn
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
@router.post("/auth/",status_code=status.HTTP_201_CREATED)
def create_user(db:dependencies,user : UserCreate):
    user_model=Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt.hash(user.password),
        role=user.role,
        is_active=True
    )
    #creation de l'utilisateur
    db.add(user_model)
    db.commit()
    return user_model

def ceation_du_token(username:str ,user_id:int, role: str,expires_delta: Optional[timedelta]=None):
    encode={"sub": username, "user_id": user_id, "role": role}
    expires_delta = timedelta(days=1)
    expires=datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth_beare)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_role= payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/token", response_model=Token)
def jwk_login(form_data : Annotated[OAuth2PasswordRequestForm,Depends()] , db:dependencies):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if user is None or not bcrypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        token=ceation_du_token(user.username, user.id,user.role, timedelta(minutes=30))
        return {"access_token": token, "token_type": "bearer"}
    
    
