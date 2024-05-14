from typing import Annotated, Optional

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from backend.apps.users.domain.token import TokenView
from backend.apps.users.security import access_token_provider, credentials_exception, refresh_token_provider

from backend.apps.users.usecases import CreateTokenUseCase, RefreshTokenUseCase
from backend.core.models import Result
from backend.core.security import TokenJWT

router = APIRouter(tags=['Users', 'Auth'])


@router.post(
    path='/api/v1/users/token',
    status_code=201,
    responses={401: {'description': 'Incorrect username/password'}},
)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], use_case: Annotated[CreateTokenUseCase, Depends()]
) -> Result[TokenView]:
    new_token = await use_case.execute(username=form_data.username, password=form_data.password)
    if not new_token:
        raise credentials_exception
    return Result(result=new_token)


@router.post(
    path='/api/v1/users/refresh-token',
    status_code=201,
    responses={401: {'description': 'Bad token'}},
)
async def refresh_token_handler(
    access_token: Annotated[Optional[TokenJWT], Depends(access_token_provider)],
    refresh_token: Annotated[Optional[str], Depends(refresh_token_provider)],
    use_case: Annotated[RefreshTokenUseCase, Depends()],
) -> Result[TokenView]:
    if not access_token or not refresh_token:
        raise credentials_exception

    new_token = await use_case.execute(access_token=access_token, refresh_token=refresh_token)

    if not new_token:
        raise credentials_exception
    return Result(result=new_token)
