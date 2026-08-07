from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemberCreate(BaseModel):
    member_name: str
    client_id: str
    password: str
    api_key: str
    totp_secret: str


class MemberUpdate(BaseModel):
    member_name: str
    client_id: str
    password: str
    api_key: str
    totp_secret: str
    is_active: bool


class MemberResponse(BaseModel):
    id: int
    member_name: str
    client_id: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)