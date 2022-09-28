from fastapi import FastAPI, HTTPException, status
from .database import engine
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

@app.get("/", status_code= status.HTTP_200_OK)
def greeting():
    greeting = "Welcome to Almari."
    return{greeting}


app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)


