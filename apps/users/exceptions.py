from zmey_gorynych.exceptions import AppError


class AccessError(AppError):
    status_code = 403
    detail = 'Доступ запрещен!'
