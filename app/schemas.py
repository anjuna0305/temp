# app/schemas.py
from typing import Optional, Union

from pydantic import BaseModel


# user schemas----------------------------------------------------------------------------------------------------------
# user base schema
class UserBase(BaseModel):
    username: str
    email: str


# create user request schema
class UserCreate(UserBase):
    scopes: str
    password: str


# update userschema
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None


# complete user class
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Update to use from_attributes


# token schemas---------------------------------------------------------------------------------------------------------
# Token base class
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data class
class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: list[str] = []


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
