from pydantic import BaseModel
from uuid import UUID


class UserOut(BaseModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
