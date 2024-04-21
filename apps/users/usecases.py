from fastapi import Depends
from starlette import status

from apps.users.exceptions import AccessError
from apps.users.repository.repository import UserRepo
from apps.users.schemas import TokenView, UserAuth
from apps.users.secure import TokenJWTFactory, PasswordHasher
from zmey_gorynych.usecases import BaseUseCase


class CreateToken(BaseUseCase):
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def execute(self, req_user: UserAuth) -> TokenView:
        user = await self.user_repo.get(req_user.username)
        if not user or not PasswordHasher.verify_password(req_user.password, user.hashed_password) or user.disabled:
            raise AccessError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password, may be user disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenJWTFactory(sub=user.username).create_token()
