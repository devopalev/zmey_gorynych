from typing import Annotated
from uuid import UUID

from fastapi import routing, Depends, HTTPException, Response

from backend.apps.devices import usecases
from backend.apps.devices.security import DeviceEventPolicy
from backend.apps.devices.domain.devices import DeviceView, TokenView
from backend.apps.devices.handlers.schemas.devices import DeviceCreateModel
from backend.apps.devices.handlers.schemas.events import Event
from backend.apps.users.security import UserPolicy, CurrentUserDep
from backend.apps.users.domain.users import User
from backend.apps.devices.event_bus import EventBus
from backend.core.models import Result

router = routing.APIRouter(tags=['Devices'])


@router.post(
    path='/api/v1/devices',
    description='Создает запись о новом устройстве',
    dependencies=[UserPolicy],
    status_code=201,
)
async def create_device(
    model: DeviceCreateModel,
    user: Annotated[User, CurrentUserDep],
    use_case: Annotated[usecases.CreateDevice, Depends(usecases.CreateDevice)],
) -> Result[DeviceView]:
    return Result(result=await use_case.execute(user_id=user.id, device_name=model.name))


@router.get(
    path='/api/v1/devices',
    description='Возвращает устройства пользователя',
    dependencies=[UserPolicy],
)
async def get_devices(
    user: Annotated[User, CurrentUserDep],
    use_case: Annotated[usecases.GetDevices, Depends(usecases.GetDevices)],
) -> Result[list[DeviceView]]:
    return Result(result=await use_case.execute(user=user))


@router.get(
    path='/api/v1/devices/{device_id}',
    description='Возвращает устройство пользователя',
    dependencies=[UserPolicy],
)
async def get_device(
    user: Annotated[User, CurrentUserDep],
    device_id: UUID,
    use_case: Annotated[usecases.GetDevice, Depends(usecases.GetDevice)],
) -> Result[DeviceView]:
    if device := await use_case.execute(user=user, uuid=device_id):
        return Result(result=device)
    else:
        raise HTTPException(status_code=404, detail='Device not found')


@router.post(
    path='/api/v1/devices/{device_id}/event',
    description='Асинхронно обрабатывает события устройств',
    status_code=201,
    dependencies=[DeviceEventPolicy],
    tags=['Events'],
)
async def send_events(
    device_id: UUID,
    event: Event,
    event_bus: Annotated[EventBus, Depends(EventBus)],
) -> Response:
    await event_bus.handle_event(device_id, event)
    return Response(status_code=201)


@router.post(
    path='/api/v1/devices/{device_id}/access-token',
    description='Обновить токен устройства',
    dependencies=[UserPolicy],
    status_code=201,
)
async def refresh_token(
    device_id: UUID,
    use_case: Annotated[usecases.CreateAccessToken, Depends(usecases.CreateAccessToken)],
) -> Result[TokenView]:
    token = await use_case.execute(device_id)
    if token:
        return Result(result=token)
    else:
        raise HTTPException(status_code=404, detail='Device not found')
