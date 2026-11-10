from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from jwt.exceptions import InvalidTokenError
import schemas, models
import jwt

from config import settings


'''
    OAuth2PasswordBearer tells FastAPI that this application uses OAuth2 bearer tokens.
    It instructs FastAPI to look at every incoming HTTP request 
    and check the Authorization header for a token that looks like:
    Authorization: Bearer <your_jwt_token>.
'''
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min


def create_access_token(data: dict, exp_delta: timedelta | None = None):
    
    payload = data.copy()
    exp_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    if exp_delta:
        expire = datetime.now(timezone.utc) + exp_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    payload.update({"exp": expire})   # we use "exp" as a key to keep the automatic expiration security that made by decode function
    payload.update({"test": "test1"})
    
    print(f"NOWWWWWWWWWWWWW: @ {datetime.now(timezone.utc)}")
    print(f"expiration date: @ {expire}")
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt



def verify_access_token(req_token: schemas.Token, credential_exception):
    try:
        '''
            The token expiration check happens automatically inside the jwt.decode() function 
            using the exp claim embedded within the token string itself.
        '''
        payload = jwt.decode(req_token, SECRET_KEY, algorithms= [ALGORITHM])
        
        user_id: int | None = payload.get("user_id")
        
        print(f"in verify_access_token function : {payload.get("test")}")
        print(f"in verify_access_token function type of payload: {type(payload)}")
        
        if not user_id:
            raise credential_exception
        
        # token_data = schemas.TokenData(id=user_id, meta=payload.get("test"))
        token_data = schemas.TokenData(id=user_id)
        print(f"in verify_access_token function : token_data value {token_data}")

    except InvalidTokenError:
        raise credential_exception
    
    return token_data


def get_current_user(token: str= Depends(oauth2_schema), db: Session = Depends(get_db)):
    '''
        1. It reads the Authorization header.
        2. If the header is missing or malformed, it automatically throws an HTTP 401 Unauthorized error right then and there.
        3. If the header exists, it strips away the word "Bearer " and passes just the raw string token into your token variable.
    '''
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Could not validate credentials", headers={"WWW-Authentication": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter_by(id= token.id).first()
    
    return user
    # return verify_access_token(token, credentials_exception)
'''

Component               	      Responsibility
-------------------------        ----------------------------------------------
OAuth2PasswordRequestForm	 =>  Reads login credentials
authenticate_user()	         =>  Verifies the username and password
create_access_token()   	 =>  Creates and signs the JWT
OAuth2PasswordBearer	     =>  Extracts the Bearer token from HTTP headers
get_current_user()      	 =>  Validates the JWT and identifies the user
Depends()	                 =>  Connects authentication to protected endpoints
-------------------------------------------------------------------------------
STEPS :::

User submits credentials
POST /token
Username + Password


Backend verifies credentials
authenticate_user()
- Find user in database.
- Verify submitted password against stored password hash.


Backend generates JWT
create_access_token()
- Add sub.
- Add exp.
- Sign using SECRET_KEY.


Backend returns the token
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}


Client stores the token
The client keeps it and includes it in subsequent protected requests.


Client requests protected resource
GET /users/me/
Authorization: Bearer eyJ...



FastAPI extracts the token
OAuth2PasswordBearer



Backend validates the token
get_current_user()
Verify signature, expiration and subject.



Backend retrieves the user
Fetch the corresponding user record and check whether the account is active.


Endpoint executes
The authenticated user is injected into the endpoint.
'''
