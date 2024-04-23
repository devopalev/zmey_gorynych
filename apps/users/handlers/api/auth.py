from typing import Annotated

from fastapi import Depends, APIRouter

from apps.users.domain.token import TokenView
from apps.users.handlers.schemas import UserAuth


from apps.users.usecases import CreateToken

router = APIRouter(tags=['Users', 'Auth'])


@router.post('/api/v1/users/token', responses={401: {'description': 'Incorrect username or password'}})
async def login_json(req_user: UserAuth, use_case: Annotated[CreateToken, Depends(CreateToken)]) -> TokenView:
    return await use_case.execute(req_user)
