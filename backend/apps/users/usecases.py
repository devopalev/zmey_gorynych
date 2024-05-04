from fastapi import Depends
from starlette import status

from backend.apps.users.exceptions import AccessError
from backend.apps.users.repository.repo import UserRepo
from backend.apps.users.handlers.schemas import UserAuth
from backend.core.security import TokenJWT
from backend.core.security import hasher
from backend.core.usecases import BaseUseCase


class CreateToken(BaseUseCase):
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def execute(self, req_user: UserAuth) -> TokenJWT:
        user = await self.user_repo.get(req_user.username)
        if not user or not hasher.verify(req_user.password, user.password_hashed) or user.revoked:
            raise AccessError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password, may be user revoked',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return TokenJWT(sub=user.username)
