from fastapi import APIRouter

from .routes import runner, tag, token

router = APIRouter()
router.include_router(tag.tag_router)
router.include_router(runner.runner_router)
router.include_router(token.token_router)
