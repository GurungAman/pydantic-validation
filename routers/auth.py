from datetime import datetime, timedelta

from fastapi import APIRouter, Cookie, Header, HTTPException
from fastapi.responses import JSONResponse
from jose import jwt

from dependencies import authenticate_user
from models import UserInRequest

router = APIRouter()

SECRET_KEY = "this-is-my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes



@router.post("/set-cookie/")
def SetCookie():
    response = JSONResponse(content="Cookie set successfully.")
    response.set_cookie(key="cookie", value="This-is-fake-session")
    return response


@router.get("/get-cookie/")
def GetCookie(cookie: str = Cookie(default=None)):
    return {"cookie": cookie}


#getting headers
@router.get("/get-headers/")
async def GetHeader(accept: str | None = Header(default=None), accept_encoding: str | None = Header(default=None), sec_ch_ua: str | None = Header(default=None)):
    return {"accpet": accept, "accept_encoding": accept_encoding, "Sec-Ch-Ua": sec_ch_ua}


# Endpoint to login and set cookie
@router.post("/login/")
async def login(user_in: UserInRequest):
    user = authenticate_user(user_in.username, user_in.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    
    response = JSONResponse(content={"message": "Login successful", "token": access_token})
    response.set_cookie(key="cookie", value="this-is-fake-session")
    return response

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



#exception handler
@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=400, detail="Item ID must be greater than 0")
    return {"item_id": item_id}