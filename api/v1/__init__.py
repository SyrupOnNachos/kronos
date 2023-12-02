from fastapi import APIRouter
from .routes import tag

router = APIRouter()
router.include_router(tag.tag_router)