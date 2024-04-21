from typing import Annotated

from fastapi import Depends, APIRouter

from apps.users.schemas import UserAuth, TokenView


from apps.users.usecases import CreateToken

api_router = APIRouter(tags=['Auth'])


@api_router.post(
    "/api/v1/users/token",
    response_model=TokenView,
    responses={401: {'description': "Incorrect username or password"}}
)
async def login_json(req_user: UserAuth, use_case: Annotated[CreateToken, Depends(CreateToken)]):
    return await use_case.execute(req_user)
