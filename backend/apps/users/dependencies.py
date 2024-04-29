from typing import Annotated, Callable

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from backend.apps.users.domain.users import User, RoleUser
from backend.apps.users.exceptions import AccessError
from backend.apps.users.repository.repo import UserRepo
from backend.apps.users.secure import TokenJWTFactory

# OAuth2PasswordBearer - достает из заголовков токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/token')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_repo: UserRepo = Depends(UserRepo)
) -> User:
    credentials_exception = AccessError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        token_factory = TokenJWTFactory.from_token(token)
    except ValueError:
        raise credentials_exception

    user = await user_repo.get(token_factory.sub)
    if not user:
        raise credentials_exception

    if user.revoked:
        raise AccessError(detail='Inactive user')

    return user


def _factory_check_role(role: RoleUser) -> Callable[[User], None]:
    def check_role(user: Annotated[User, Depends(get_current_user)]) -> None:
        if RoleUser.is_admin(user):
            return
        elif role not in user.roles:
            raise AccessError(detail='Access denied')

    return check_role


SecureAdminDep = Depends(_factory_check_role(RoleUser.ADMIN))
SecureUserDep = Depends(_factory_check_role(RoleUser.USER))
