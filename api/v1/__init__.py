from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1.routes.dependencies import get_current_user
from models import get_db

from .routes import callback, connection, runner, tag, user

router = APIRouter()


@router.get("/health_check")
def health_check(db: Session = Depends(get_db)):
    # Check if db is alive
    try:
        db.execute("SELECT 1")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database is not alive: {e}")

    return {"status": 200, "message": "Ok"}


router.include_router(tag.tag_router, dependencies=[Depends(get_current_user)])
router.include_router(runner.runner_router, dependencies=[Depends(get_current_user)])
router.include_router(
    connection.connection_router, dependencies=[Depends(get_current_user)]
)
router.include_router(callback.callback_router)
router.include_router(user.user_router)
