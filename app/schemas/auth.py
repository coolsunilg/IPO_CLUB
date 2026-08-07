from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BulkLoginRequest(BaseModel):
    member_ids: list[int]