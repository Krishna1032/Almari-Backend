from fastapi import FastAPI
from .database import engine
from .import models
from .routers import login, users, posts

models.Base.metadata.create_all(bind=engine)

app =  FastAPI()

app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)


