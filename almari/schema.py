from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


#schema for users
class SignupModel(BaseModel):
    email: EmailStr
    password: str

class ReturnUser(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode = True

#schema for token
class Token(BaseModel):
    access_token:str
    token_type: str

class Tokendata(BaseModel):
    id: Optional [str] = None


class PostBase(BaseModel):
    category: str
    title: str
    description: str
    post_img: str
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: ReturnUser

    class Config: #converts sequel alchemy model into pydantic model
        orm_mode = True


