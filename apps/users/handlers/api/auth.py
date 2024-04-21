from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter

from apps.users.schemas import UserAuth, TokenView
from apps.users.secure import TokenJWTFactory
from fastapi.security import OAuth2PasswordRequestForm

api_router = APIRouter(tags=['Auth'])


@api_router.post(
    "/api/v1/users/token",
    response_model=TokenView,
    responses={401: {'description': "Incorrect username or password"}}
)
async def login_json(req_user: UserAuth, user_repo: UserRepo = Depends(UserRepo)):
    user = await authenticate_user(session, req_user.username, req_user.password)
    return TokenJWTFactory(user.sub).create_token()
