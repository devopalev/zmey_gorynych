from typing import Annotated

from fastapi import Depends, status, Security
from fastapi.security import OAuth2PasswordBearer

from apps.users.domain.users import User, RoleUser
from apps.users.exceptions import AccessError
from apps.users.repository.repository import UserRepo
from apps.users.secure import TokenJWTFactory

# OAuth2PasswordBearer - достает из заголовков токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/form/auth")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           user_repo: UserRepo = Depends(UserRepo)) -> User:
    credentials_exception = AccessError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token = TokenJWTFactory.from_token(token)
    except ValueError:
        raise credentials_exception

    user = await user_repo.get(token.sub)
    if not user:
        raise credentials_exception

    if user.disabled:
        raise AccessError(detail="Inactive user")

    return user


def _factory_check_role(role: RoleUser):
    def check_role(user: Annotated[User, Security(get_current_user)]):
        if RoleUser.is_admin(user):
            return user
        elif role not in user.roles:
            raise AccessError(detail="Missing role")

    return check_role


SecureAdminDep = Depends(_factory_check_role(RoleUser.ADMIN))
SecureUserDep = Depends(_factory_check_role(RoleUser.USER))
