from typing import Optional, Dict, Any

from fastapi.exceptions import HTTPException


class AppException(HTTPException):
    status_code: int = 500
    detail: Any = 'Упс... что-то пошло не так'

    def __init__(self, status_code: Optional[int] = None, detail: Any = None, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=status_code or self.status_code, detail=detail or self.detail, headers=headers)
