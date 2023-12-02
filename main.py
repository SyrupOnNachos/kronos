from fastapi import FastAPI
from api import api_router

app = FastAPI()

# Include the router from tag.py
app.include_router(api_router)
