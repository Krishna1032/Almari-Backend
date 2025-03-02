from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schema, utils
from typing import List


router = APIRouter(prefix="/cart", tags=["Cart"])


# create a cart item
@router.post(
    "/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.CartOut
)
def create_item(
    id: int,
    item: schema.CartAdd,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    new_item = models.Cart(owner_id=current_user.id, product_id=id, **(item.dict()))
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# get all cart items of the user
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.CartOut])
def getAllItems(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    user_id = current_user.id
    items = db.query(models.Cart).filter(models.Cart.owner_id == user_id).all()
    return items


# delete a cart item of the user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    query = db.query(models.Cart).filter(models.Cart.id == id)
    item = query.first()

    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id:{id} not found"
        )

    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized"
        )

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update the cart item of the user
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.CartOut)
def update_item(
    updated_item: schema.CartAdd,
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    query = db.query(models.Cart).filter(models.Cart.id == id)
    item = query.first()
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id:{id} not found"
        )

    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized"
        )

    query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return query.first()
