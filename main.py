from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router from tag.py
app.include_router(api_router)
