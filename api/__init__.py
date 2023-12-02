from fastapi import APIRouter
from api.v1 import router

api_router = APIRouter()

# Include the router from tag.py
api_router.include_router(router)
