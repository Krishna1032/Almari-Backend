from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schema
from typing import List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)
