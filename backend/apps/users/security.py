import logging
from typing import Annotated, Callable, Optional

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader

from backend.apps.users.domain.token import TokenView
from backend.apps.users.domain.users import User, RoleUser
from backend.apps.users.exceptions import AccessError
from backend.apps.users.repository.repo import UserRepo
from backend.core.security import TokenJWT


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/token', auto_error=False)
refresh_token_provider = APIKeyHeader(name=TokenView.refresh_header_name, auto_error=False)

credentials_exception = AccessError(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


async def access_token_provider(token: str = Depends(oauth2_scheme)) -> Optional[TokenJWT]:
    if not token:
        return None

    try:
        return TokenJWT.from_token(token)
    except ValueError:
        logging.warning('Token decode error')
        return None


async def _get_current_user(
    token_jwt: TokenJWT = Depends(access_token_provider),
    user_repo: UserRepo = Depends(UserRepo),
) -> User:
    if not token_jwt:
        raise credentials_exception

    user = await user_repo.get(user_id=token_jwt.user_id)
    if not user:
        logging.warning(f'User(id={token_jwt.user_id}) not found')
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
