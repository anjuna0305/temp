from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class InternalServerError(HTTPException):
    def __init__(self, status_code: int = 500, detail: Any = "Internal server error."):
        super().__init__(status_code, detail=detail)


class InvalidFormatError(HTTPException):
    def __init__(self, status_code: int = 400, detail: Any = "Invalid format."):
        super().__init__(status_code, detail=detail)


# raise HTTPException(status_code=404, detail="User not found")
class NotFoundError(HTTPException):
    def __init__(self, status_code: int = 404, detail: Any = "Not found.") -> None:
        super().__init__(status_code, detail)


class ConflictError(HTTPException):
    def __init__(self, status_code:int = 409, detail:Any = "Conflict in input data.")->None:
        super().__init__(status_code, detail)