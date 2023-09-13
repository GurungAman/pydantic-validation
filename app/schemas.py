from datetime import datetime
from typing import Annotated, Any, List, Optional
from uuid import UUID

from fastapi import Form, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field, HttpUrl, validator
from pydantic.networks import EmailStr, IPvAnyAddress
from pydantic_extra_types.color import Color
from pydantic_extra_types.coordinate import Coordinate
from pydantic_extra_types.mac_address import MacAddress

from app.utils import as_form


class BaseUserSchema(BaseModel):
    email: EmailStr
    user_name: str 
    first_name: str
    # middle_name: str | None = None
    middle_name: Optional[str] = None
    last_name: str 
    address: str | None

    

class RequestUserSchema(BaseUserSchema):
    # password: str
    password: Annotated[str, Field(min_length=10)]
    confirm_password: str


    @validator("password")
    def validate_password(cls, value):
        # perform validations
        if len(value) < 6:
            raise HTTPException(
                status_code=400,
                detail="Invalid password",
            )
        return value
    
    @validator("confirm_password")
    def validate_passwords_match(cls, confirm_password, values):
        if "password" in values and confirm_password != values["password"]:
            raise HTTPException(
                status_code = 400, 
                detail = "Passwords do not match"
                )
        return confirm_password

class ResponseUserSchema(BaseUserSchema):
    id: int


class Book(BaseModel):
    title : str
    author: str
    price: float = Query(gt=0, default=20.00, description="The price must be greater than zero")


class Tag(BaseModel):
    name: str
    book_id: int
    
    @validator("book_id", pre=False)
    def validate_name(cls, value):
        return value

class RequestBookSchema(BaseModel):
    book: Book
    tags: Optional[List[Tag]] = None
    
    @validator("tags", pre=True)
    def validate_tags_length(cls, tags):
        if tags is None:
            return None
        if len(tags) > 5:
            raise ValueError("Tags list should not contain more than 5 elements")
        return tags


class ResponseBookSchema(BaseModel):
    book: Book
    tags: List[Tag] = []


class ExtraTypeRequest(BaseModel):
    uuid: Annotated[UUID, None] = None
    date_time: Annotated[datetime, None] = None
    email: Annotated[EmailStr, None] = None
    link: Annotated[HttpUrl, None] = None
    coordinate: Annotated[Coordinate, None] = None
    ip_address: Annotated[IPvAnyAddress, None] = None
    color: Annotated[Color, None] = None
    mac_address: Annotated[MacAddress, None] = None
    

class FormData(BaseModel):
    name: Annotated[str, Form()]
    address: Annotated[str, Form()]
    file: Annotated[str, UploadFile]
    
    @validator("file")
    def validate_file(cls, file):
        if file.size > 1 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large.")
        return file
    
    
class FileName(BaseModel):
    file_name: str
