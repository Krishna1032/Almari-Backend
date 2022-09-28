from fastapi import FastAPI
from .database import engine
from .import models
from .routers import login, users, posts
from fastapi.middleware.cors import CORSMiddleware
origins =["*"]
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app =  FastAPI()

app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)


