from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    success: Optional[bool] = Field(True, description="Всегда true")
    data: T = Field(..., description="Полезная нагрузка")

class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Машиночитаемый код ошибки")
    message: str = Field(..., description="Человеко-читаемое сообщение")
    details: dict = Field(default_factory=dict, description="Дополнительные сведения")

class ErrorResponse(BaseModel):
    success: Optional[bool] = Field(False, description="Всегда false")
    error: ErrorDetail