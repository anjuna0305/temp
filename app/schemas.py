# app/schemas.py
from typing import Optional, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Update to use from_attributes


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class APIServiceBase(BaseModel):
    name: str
    description: Optional[str] = None


class APIServiceCreate(APIServiceBase):
    pass


class APIService(APIServiceBase):
    id: int

    class Config:
        from_attributes = True  # Update to use from_attributes


class UserAPIServiceBase(BaseModel):
    user_id: int
    api_service_id: int
    status: str


class UserAPIServiceCreate(UserAPIServiceBase):
    pass


class UserAPIService(UserAPIServiceBase):
    id: int

    class Config:
        from_attributes = True  # Update to use from_attributes


class ActivityLogBase(BaseModel):
    user_id: int
    api_service_id: int
    action: str
    detail: Optional[str] = None


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLog(ActivityLogBase):
    id: int

    class Config:
        from_attributes = True  # Update to use from_attributes
