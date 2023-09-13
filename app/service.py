import shutil

from fastapi import HTTPException

from app.db import user_db
from app.schemas import ResponseUserSchema

save_path = "uploads/"

class UserService:
    def create_user(self, user):
        user_data = user.model_dump()
        id = len(user_db) + 1
        for data in user_db:
            if data["email"] == user_data["email"]:
                raise HTTPException(
                    status_code = 400, 
                    detail =  "Email already exists.",
                    )
            if data["user_name"] == user_data["user_name"]:
                raise HTTPException(
                    status_code = 400, 
                    detail ="Username already exists.",
                    )
        user_data["id"] = id
        user_db.append(user_data)
        return user_data

    def get_user(self, user_id):
        for user_data in user_db:
            if user_data["id"] == user_id:
                return user_data
                # return ResponseUserSchema(**user_data)
        raise HTTPException(
            status_code = 400, 
            detail ="User not found.",
            )
    
    def list_users(self):
        user_data = []
        for data in user_db:
            user_data.append(ResponseUserSchema(**data))
        return user_data


def save_file(file):
    file_path = save_path + file.filename
    with open(file_path, "wb") as destination:
        shutil.copyfileobj(file.file, destination)
    return