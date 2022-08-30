from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schema
from typing import List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)
@router.post("/", status_code = status.HTTP_201_CREATED)
def createpost(post: schema.PostCreate,  db: Session = Depends(database.get_db), 
                current_user: int = Depends(oauth2.get_current_user)): 
    print (post)   
    new_post = models.Posts(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


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

@router.put("/{id}", response_model= schema.Post)
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


@router.get("/", status_code = status.HTTP_200_OK, response_model= List[schema.Post])
def getAllPosts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Posts).all()
    return posts

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model= schema.Post)
def getOnePost(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 
        f"The post with id {id} not found")
    return post

