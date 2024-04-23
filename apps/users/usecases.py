from abc import ABC
from typing import cast

from fastapi import Depends
from passlib.context import CryptContext
from starlette import status

from apps.users.domain.token import TokenView
from apps.users.exceptions import AccessError
from apps.users.repository.repo import UserRepo
from apps.users.handlers.schemas import UserAuth
from apps.users.secure import TokenJWTFactory
from core.usecases import BaseUseCase


class PasswordUseCase(BaseUseCase, ABC):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return cast(bool, self.pwd_context.verify(plain_password, hashed_password))

    def _hash_password(self, password: str) -> str:
        return cast(str, self.pwd_context.hash(password))


class CreateToken(PasswordUseCase):
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def execute(self, req_user: UserAuth) -> TokenView:
        user = await self.user_repo.get(req_user.username)
        if not user or not self._verify_password(req_user.password, user.password_hashed) or user.revoked:
            raise AccessError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password, may be user revoked',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return TokenJWTFactory(sub=user.username).create_token()
