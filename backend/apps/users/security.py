from typing import Annotated, Callable, Optional

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from backend.apps.users.domain.users import User, RoleUser
from backend.apps.users.exceptions import AccessError
from backend.apps.users.repository.repo import UserRepo
from backend.core.security import TokenJWT


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/token', auto_error=False)

credentials_exception = AccessError(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


async def jwt_provider(token: str = Depends(oauth2_scheme)) -> Optional[TokenJWT]:
    if not token:
        return None
    try:
        return TokenJWT.from_token(token)
    except ValueError:
        return None


async def _get_current_user(
    token_jwt: TokenJWT = Depends(jwt_provider),
    user_repo: UserRepo = Depends(UserRepo),
) -> User:
    if not token_jwt:
        raise credentials_exception

    user = await user_repo.get(token_jwt.sub)
    if not user:
        raise credentials_exception

    if user.revoked:
        raise AccessError(detail='Inactive user')

    return user


def _factory_check_role(role: RoleUser) -> Callable[[User], None]:
    def check_role(user: Annotated[User, Depends(_get_current_user)]) -> None:
        if RoleUser.is_admin(user):
            return
        elif role not in user.roles:
            raise AccessError(detail='Access denied')

    return check_role


CurrentUserDep = Depends(_get_current_user)
AdminPolicy = Depends(_factory_check_role(RoleUser.ADMIN))
UserPolicy = Depends(_factory_check_role(RoleUser.USER))
