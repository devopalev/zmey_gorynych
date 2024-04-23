from typing import Annotated
from uuid import UUID

from fastapi import routing, Depends, HTTPException, Response

from apps.devices import usecases
from apps.devices.domain.devices import DeviceView
from apps.devices.handlers.schemas.devices import DeviceCreateModel
from apps.devices.handlers.schemas.events import Event
from apps.users.dependencies import SecureUserDep, get_current_user
from apps.users.domain.users import User
from apps.devices.event_bus import EventBus

router = routing.APIRouter(tags=['Devices'])


@router.post(path='/api/v1/devices', description='Создает запись об новом устройстве', dependencies=[SecureUserDep])
async def create_device(
    model: DeviceCreateModel,
    user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[usecases.CreateDevice, Depends(usecases.CreateDevice)],
) -> DeviceView:
    return await use_case.execute(user_id=user.id, device_name=model.name)


@router.get(
    path='/api/v1/devices/{device_id}',
    description='Возвращает устройство пользователя',
    dependencies=[SecureUserDep],
)
async def get_device(
    device_id: UUID, use_case: Annotated[usecases.GetDevice, Depends(usecases.GetDevice)]
) -> DeviceView:
    if device := await use_case.execute(device_id):
        return device
    else:
        raise HTTPException(status_code=404, detail='Device not found')


@router.post(
    path='/api/v1/devices/{device_uuid}/event',
    description='Асинхронно обрабатывает события устройств',
    dependencies=[SecureUserDep],
    tags=['Events'],
)
async def send_events(device_uuid: UUID, event: Event, event_bus: Annotated[EventBus, Depends(EventBus)]) -> Response:
    await event_bus.handle_event(device_uuid, event)
    return Response(status_code=201)
