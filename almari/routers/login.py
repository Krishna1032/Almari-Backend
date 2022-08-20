from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import oauth2, models, utils, schema, database

router = APIRouter(
    prefix = "/login",
    tags = ['Authentication']
)

@router.get("/", status_code= status.HTTP_202_ACCEPTED, response_model= schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
        detail= f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
        detail= f"Invalid Credentials")

    #create a token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    #return a token
    return{"access_token": access_token, "token_type" : "bearer"}