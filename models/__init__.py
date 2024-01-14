from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv('SNOWFLAKE_USERNAME')
PASSWORD=os.getenv('SNOWFLAKE_PASSWORD')
ACCOUNT_ID=os.getenv('SNOWFLAKE_ACCOUNT_ID')
DB_NAME=os.getenv('SNOWFLAKE_DB_NAME')
SCHEMA_NAME=os.getenv('SNOWFLAKE_SCHEMA_NAME')

snowflake_db = f'snowflake://{USER}:{PASSWORD}@{ACCOUNT_ID}/{DB_NAME}/{SCHEMA_NAME}'

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
