from pydantic import BaseModel


class User(BaseModel):
    username: str
    password_hash: str

class UserInResponse(User):
    pass

class UserInRequest(BaseModel):
    username: str
    password: str



class Item(BaseModel):
    name: str
    description: str = None
    price: float
