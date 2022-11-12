from fastapi import FastAPI, status
from .database import engine
from . import models
from .routers import login, users, posts, cart
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins =["*"]
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code= status.HTTP_200_OK)
def greeting():
    greeting = "Welcome to Almari."
    return{greeting}


app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(cart.router)


