from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import User

SECRET_KEY = "this-is-my-secret-key"
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simulated database of users
users_db = {
    "alice": User(username="alice", password_hash=password_context.hash("alicepass")),
    "bob": User(username="bob", password_hash=password_context.hash("bobpass")),
}

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and verify_password(password, user.password_hash):
        return user


# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#get header
def get_header_token(authorization: str = Header()):
    if authorization and authorization.startswith("Bearer"):
        token = authorization.split(" ")[1]
        return token

# Dependency to get authenticated user  
def get_current_user(token: str = Depends(get_header_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = users_db.get(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
