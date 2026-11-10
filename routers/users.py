from fastapi import APIRouter, HTTPException, status, Response, Depends
from database import get_db
from sqlalchemy.orm import Session
import models, schemas, tokengen
from typing import List



###################################### Global Variables ######################################
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



###################################### Helper Functions ######################################
from utils import hash_password

###################################### APIs ######################################

@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    print(type(users))
    return users

@router.get("/{user_id}", response_model=List[schemas.UserResponse])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=user_id).first()
    print(type(user))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the user with id:{user_id} not found')
    return [user]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), get_current_user: int = Depends(tokengen.get_current_user)):
    
    print("Password length:", len(user.password))
    print("Password bytes:", len(user.password.encode("utf-8")))
    
    # hash the password
    user.password = hash_password(user.password)
    
    payload = models.User(**user.model_dump())
    db.add(payload)
    db.commit()
    db.refresh(payload)
    return payload

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user_id: int, db: Session = Depends(get_db)):  
    target_user = db.query(models.User).filter_by(id=user_id).first()
    if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the user with id:{user_id} not found')
    db.delete(target_user)
    db.commit()
    return {'result': f'Post with id {user_id} is deleted'}

@router.put("/{user_id}")
async def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter_by(id=user_id)
    target_user = user_query.update({**user.model_dump()})
    
    print(type({**user.model_dump()}))
    print(type(target_user))
    
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the user with id:{user_id} not found')
    db.commit()    # push changes from staging to the database
    return {'msg':'user updated', 'data':user_query.first()}



@router.patch("/{user_id}", response_model=List[schemas.UserResponse])
async def patch_user(user_id: int, user: schemas.UserPATCH, db: Session = Depends(get_db)):
    
    payload_user = user.model_dump(exclude_unset=True) 
    target_user = db.query(models.User).filter_by(id=user_id).update(payload_user)
    print(type(payload_user))
    if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the user with id:{user_id} not found')
    db.commit()   
    target_user = db.query(models.User).filter_by(id=user_id).first()   # re-fetch
    return [target_user]
