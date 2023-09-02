from fastapi import APIRouter, Cookie, Depends

from dependencies import get_current_user
from models import UserInResponse

router = APIRouter()

# Protected endpoint that requires authentication

#getting user's username from cookie token
@router.get("/protected/home/")
async def Home(user: UserInResponse = Depends(get_current_user)):
    return {"message": f"Welcome, {user.username}!"}


@router.get("/protected/get-cookie/")
async def Home(cookie: str = Cookie(default=None)):
    return {"cookie": cookie}

