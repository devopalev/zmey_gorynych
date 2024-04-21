import logging
from uuid import UUID

from apps.devices.handlers.schemas import stats


async def handle_event(device_id: UUID, event: stats.Event):
    match event.type:
        case event.type.TEST:
            logging.info('Test OKey!')
        case event.type.KEEP_ALIVE:
            logging.warning('НЕ реализовано, но скоро будет')
        case _:
            logging.error('Неизвестный event!')
