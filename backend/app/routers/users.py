from datetime import timedelta
from typing import Union

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import create_access_token, verify_password
from errors import IntegrityErrorException
from models import User, Player
from models.auth import Token
from models.user import UserExternal
from queries.user import save_user, get_current_active_user
from queries.user import get_user_by_username
from settings import Settings

login_router = APIRouter(
    prefix="/token",
    tags=["token"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)

user_router_no_auth_required = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


def authenticate_user(username: str, password: str) -> Union[User, bool]:
    user = get_user_by_username(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@login_router.post("", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserExternal)
async def route_read_users_me(current_user: User = Depends(get_current_active_user)):
    current_user.__delattr__('password')
    return current_user


@user_router_no_auth_required.post("", response_model=User)
async def route_create_user(user: User):
    try:
        user_db = save_user(user)
        if user_db:
            Player(handicap=22.5, user_id=user_db.id).save()
        return user_db
    except IntegrityErrorException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=exc.message)

