from pydantic import BaseModel, EmailStr
from datetime import datetime


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