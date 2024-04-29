from typing import Annotated

from fastapi import Depends, APIRouter

from backend.apps.users.domain.token import TokenView
from backend.apps.users.handlers.schemas import UserAuth, TokenSchema

from backend.apps.users.usecases import CreateToken

router = APIRouter(tags=['Users', 'Auth'])


@router.post(
    path='/api/v1/users/token',
    response_model=TokenSchema,
    status_code=201,
    responses={401: {'description': 'Incorrect username or password'}},
)
async def create_token(req_user: UserAuth, use_case: Annotated[CreateToken, Depends(CreateToken)]) -> TokenView:
    return await use_case.execute(req_user)
