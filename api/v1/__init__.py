from fastapi import APIRouter
from .routes import tag
from.routes import runner

router = APIRouter()
router.include_router(tag.tag_router)
router.include_router(runner.runner_router)