from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from .tag import Tag

SQLALCHEMY_DATABASE_URL = "sqlite:///./kronos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database():
    Base.metadata.create_all(bind=engine)

# Call this function at the beginning of your application startup
create_database()
