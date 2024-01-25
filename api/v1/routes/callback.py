from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.v1.routes.connection import create_connection
from api.v1.schema.request.utils import Service
from models import get_db
from models.token import Token
from utils.connection import generate_spotify_credentials

app = FastAPI()

callback_router = APIRouter(prefix="/callbacks", tags=["callbacks"])


@callback_router.get("/spotify")
def spotify_callback(code: str, state: str, db: Session = Depends(get_db)):
    status_code, response = generate_spotify_credentials(code)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)

    token = db.query(Token).filter(Token.id == state).first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = token.user

    # Redirect to the create_connection API with the new auth token in the Authorization header
    response = create_connection(
        service=Service.spotify,
        auth_token=response.get("access_token"),
        expires_in_seconds=response.get("expires_in"),
        meta_data=response,
        db=db,
        current_user=current_user,
    )

    return response
