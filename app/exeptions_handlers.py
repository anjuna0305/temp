from fastapi import HTTPException


class InternalServerError(HTTPException):
    def __init__(self, detail: str = None):
        if detail is None:
            detail = "Internal server error."
        super().__init__(status_code=500, detail=detail)
