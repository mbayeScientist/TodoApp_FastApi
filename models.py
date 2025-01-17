from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Todo(Base):
    #nom de la table
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(Integer, index=True)
    complete= Column(Boolean, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
class Users(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String, index=True)
    is_active = Column(Boolean, index=True)
    role= Column(String, index=True)
    
    
    