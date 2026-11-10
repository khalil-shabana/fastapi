from passlib.context import CryptContext
from pwdlib import PasswordHash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(plain_pass, hashed_pass)
