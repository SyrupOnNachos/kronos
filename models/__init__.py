from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from .tag import Tag

user='amazz'
password='kJrrBPp3ti1q'
account_identifier='zyalpqw-qh50879'

db_name='kronos'
schema_name='public'
snowflake_db = f'snowflake://{user}:{password}@{account_identifier}/{db_name}/{schema_name}'

engine = create_engine(snowflake_db)
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
