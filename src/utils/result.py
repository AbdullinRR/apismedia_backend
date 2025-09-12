from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=str)

class Result(BaseModel, Generic[T, E]):
    ok: bool
    data: T | None = None
    error: E | None = None

    @classmethod
    def success(cls, data: T) -> "Result[T, E]":
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, error: E) -> "Result[T, E]":
        return cls(ok=False, error=error)
