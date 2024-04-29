import logging
from uuid import UUID

from fastapi import BackgroundTasks

from backend.apps.devices.exceptions import UnknownEventError
from backend.apps.devices.handlers.schemas.events import Event
from backend.apps.devices.repository.repo import DeviceRepo


class EventBus:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    async def handle_event(self, device_id: UUID, event: Event) -> None:
        match event.type:
            case event.type.TEST:
                logging.info('Test OKey!')
            case event.type.KEEP_ALIVE:
                self.background_tasks.add_task(DeviceRepo.update_activity, device_id)
            case _:
                raise UnknownEventError()
