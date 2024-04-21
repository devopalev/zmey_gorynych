from uuid import UUID

from fastapi import routing, BackgroundTasks
from apps.devices.handlers.schemas.stats import Event
from apps.users.dependencies import SecureUserDep
from zmey_gorynych.events_bus.devices import handle_event

router = routing.APIRouter()
TAG_DEVICES = ('Devices',)


@router.post(
    path='/api/v1/devices',
    description='Создает запись об новом устройстве',
    dependencies=[SecureUserDep],
    tags=TAG_DEVICES
)
async def create_device():
    return {"message": f"Hello {name}"}


@router.get(
    path='/api/v1/devices',
    description='Возвращает устройства пользователя',
    dependencies=[SecureUserDep],
    tags=TAG_DEVICES
)
async def get_device():
    return {"message": f"Hello {name}"}


@router.post(
    path='/api/v1/devices/{device_uuid}/event',
    description='Асинхронно обрабатывает события устройств',
    dependencies=[SecureUserDep],
    tags=(*TAG_DEVICES, 'Events')
)
async def send_events(device_uuid: UUID, event: Event, background_tasks: BackgroundTasks):
    background_tasks.add_task(handle_event, device_uuid, event)


@router.get(
    path="/api/v1/devices/{device_id}/activity",
    dependencies=[SecureUserDep],
    response_model=None,
    tags=TAG_DEVICES
)
async def get_last_activity(device_id: int) -> None:
    return {"message": "Hello"}
