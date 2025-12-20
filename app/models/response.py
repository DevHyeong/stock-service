from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    '''통일된 API 응답 형식'''
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    '''에러 응답'''
    success: bool = False
    message: str
    error: str