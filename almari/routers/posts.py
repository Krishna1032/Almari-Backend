import shutil
from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends, Response
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schema, utils
import secrets
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)


# static file setup config


# create post 
@router.post("/", status_code = status.HTTP_201_CREATED)
def createpost(post: schema.PostCreate = Depends(), db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), file:UploadFile = File(...)):

    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension not allowed"}
    
    token_name = secrets.token_hex(10) + "." + extension
    url = str("images/" + token_name)

    with open(url, "wb") as image:
        shutil.copyfileobj(file.file, image)

    new_post = models.Posts(owner_id = current_user.id, post_img = url, **(post.dict()))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# delete a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db : Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Not Authorized")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT) #in delete we usually don't return anything so only the response is given


# update a post
@router.put("/{id}", response_model= schema.PostOut)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(database.get_db),
current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Not Authorized")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()


# get all posts
@router.get("/", status_code = status.HTTP_200_OK, response_model= List[schema.PostOut])
def getAllPosts(search: Optional[str]="", limit: int = 5, skip: int = 0, db: Session = Depends(database.get_db)):

    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# get one post
@router.get("/{id}", status_code = status.HTTP_200_OK, response_model= schema.PostOut)
def getOnePost(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 
        f"The post with id {id} not found")
    return post

