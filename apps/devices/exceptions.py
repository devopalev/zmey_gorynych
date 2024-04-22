from core.exceptions import AppException


class UnknownEventError(AppException):
    status_code = 500
    detail = 'Не удалось распознать и обработать event'
