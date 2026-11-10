from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from sqlalchemy.orm import Session
import models, schemas, tokengen
from typing import List
from utils import verify_password

###################################### Global Variables ######################################
router = APIRouter(
    tags=["Authentication"]
)



###################################### APIs ######################################

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
        OAuth2PasswordRequestForm is a built-in FastAPI dependency class that parses form data
        is this case the key fields won't be {"email": xx, "password": xx} but it will be {"username": xx, "password": xx}
    '''
    login_user= db.query(models.User)\
        .filter_by(email=user_credentials.username)\
        .first() # Note we here used username: not email as in User Schema
    
    print (f"In login function: type of login_user: {type(login_user)}")
    print (f"In login function: type of user_credentials: {type(user_credentials)}")
    print (f"In login function: value of user_credentials.username: {user_credentials.username}")
    
    if not login_user or\
       not verify_password(user_credentials.password, login_user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect email or password')
    
    access_token = tokengen.create_access_token(data = {"user_id": login_user.id})
    print(f"user_id: {login_user.id}")
    
    return {"access_token": access_token, "token_type": "bearer", "user_id": login_user.id}


