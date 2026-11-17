from datetime import datetime
from models import User, Post
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, Literal



class User(BaseModel):
    email:EmailStr
    password:str
    phone_num: Optional[str] = None
class UserCreate(User):
    pass

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
class UserPATCH(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    
class UserLogin(User):
    pass


#########################################################################################

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class VoteResponse(BaseModel):
    vote_count: int
    
########################################################################################


class Post_PATCH(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    #rating: Optional[int] = None
    
class Post(BaseModel):
    title:str
    content: str
    published: Optional[bool] = None 
    #rating: Optional[int] = None
    
class PostCreate(Post):
    # user_id: int
    pass
    # title:str
    # content: str
    # published: Optional[bool] = None 
    #rating: Optional[int] = None

class PostResponse(Post):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse
    #rating: Optional[int] = None
    

class PostOut(BaseModel):
    Post: PostResponse      # your existing post response schema
    votes: int

    # model_config = ConfigDict(from_attributes=True)   # Pydantic v2
    
#########################################################################################


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    
class TokenData(BaseModel):
    id: Optional[int]
    meta: Optional[str] = None
