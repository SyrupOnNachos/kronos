from datetime import datetime

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from api.v1.schema.request.user import LoginRequest, LogoutRequest
from models import get_db
from models.token import Token
from models.user import User

app = FastAPI()

user_router = APIRouter(prefix="/users", tags=["users"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_router.post("/")
def create_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this username",
        )

    hashed_password = pwd_context.hash(password)
    user = User(
        username=username,
        password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@user_router.post("/login")
def login_user(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    body = body.dict()
    user = db.query(User).filter(User.username == body.get("username")).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
        )

    if not pwd_context.verify(body.get("password"), user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    token = db.query(Token).filter(Token.user_id == user.id).first()
    if not token:
        token = Token(user_id=user.id)
        db.add(token)
        db.commit()
        db.refresh(token)
    elif token.expires_on < datetime.utcnow():
        db.delete(token)
        db.commit()
        token = Token(user_id=user.id)
        db.add(token)
        db.commit()
        db.refresh(token)

    return {"status": 200, "token": token.id, "expires_on": token.expires_on}


@user_router.post("/logout")
def logout_user(
    body: LogoutRequest,
    db: Session = Depends(get_db),
):
    body = body.dict()
    token_id = body.get("token")

    # Find the user associated with the token and delete all tokens associated with that user
    token = db.query(Token).filter(Token.id == token_id).first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token does not exist. User already logged out.",
        )
    tokens = db.query(Token).filter(Token.user_id == token.user_id).all()
    for token in tokens:
        db.delete(token)
        db.commit()

    return {"status": status.HTTP_200_OK, "message": "User logged out"}
