
#relions la base de donnees postgresql a notre application
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#on cree un moteur de base de donnees
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" #pour des besoins de tests deploiement

#on cree une session de base de donnees
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
#on cree une session de base de donnees
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#on cree une base de donnees
Base = declarative_base()
        


