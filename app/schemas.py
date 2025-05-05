from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated


class BaseUser(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PayloadUser(BaseUser):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BasePost):
    id: int
    created_at: datetime
    user_id: int
    owner: User
    votes: int

    class Config:
        from_attributes = True


class PayloadPost(BasePost):
    pass



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1)
    class Config:
        from_attributes = True