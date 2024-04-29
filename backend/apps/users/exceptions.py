from backend.core.exceptions import AppException


class AccessError(AppException):
    status_code = 403
    detail = 'Доступ запрещен!'
