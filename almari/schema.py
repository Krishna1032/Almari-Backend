from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


#schema for users
class SignupModel(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    password: str

class ReturnUser(BaseModel):
    id:int
    email: EmailStr
    name: str
    phone_number: str
    created_at: datetime

    class Config: 
        orm_mode = True


#schema for token
class Token(BaseModel):
    access_token:str
    token_type: str

class Tokendata(BaseModel):
    id: Optional [str] = None


# schema for posts
class PostBase(BaseModel):
    category: str
    title: str
    description: str
    price: int

    class Config: #converts sequel alchemy model into pydantic model
        orm_mode = True
    
class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: ReturnUser

    


#schema for cart
class CartBase(BaseModel):
    quantity: int

    class Config:
        orm_mode = True

class CartAdd(CartBase):
    pass

class CartOut(CartBase):
    id: int
    owner_id: int
    product_id: int
    product: PostBase

   