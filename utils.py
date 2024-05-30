from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = 'TEST01'   # should be kept secret
JWT_REFRESH_SECRET_KEY ='TEST02' 

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #context for hashing password

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_hashed_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def verify_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM) 
    email = (payload.get('sub'))
    if email is None:
        return "No email"
    return email
        

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    # recalculate the expiry  of token time
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else: 
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None: 
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
