from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import create_access_token
from auth.user import get_current_active_user, authenticate_user, create_dict_for_access_token
from models.auth import Token
from models.user import User
from schemas.user import UserSchema, UserExternalSchema
from services.user import UserService
from settings import Settings
from utils.errors import IntegrityErrorException

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
        data=create_dict_for_access_token(username=user.username),
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserExternalSchema)
async def route_read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserExternalSchema(**current_user.__dict__)


@user_router_no_auth_required.post("", response_model=UserExternalSchema)
async def route_create_user(user: UserSchema):
    try:
        user_model = User(**user.dict())
        created_user = UserService().create_user(user_model)
        return UserExternalSchema(**created_user.__dict__)
    except IntegrityErrorException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Another user was created with that data')


@user_router_no_auth_required.get("/activate")
async def route_activate_user(activation_code: str):
    try:
        UserService().activate_user(activation_code=activation_code)
        return {'message': 'User Activated'}
    except IntegrityErrorException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=exc.message)
    pass


@user_router_no_auth_required.post("/reset-password")
async def reset_password_user(email: str):
    return {'message': 'Email sent'}

