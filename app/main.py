import json
import os
from typing import Annotated, Any, List

from fastapi import FastAPI, File, Form, HTTPException, Path, Request, UploadFile
from fastapi.responses import FileResponse

from app.schemas import (
    ExtraTypeRequest,
    FileName,
    FormData,
    RequestBookSchema,
    RequestUserSchema,
    ResponseBookSchema,
    ResponseUserSchema,
)
from app.service import UserService, save_file, save_path

app = FastAPI()
user_service = UserService()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/body/")
async def body(
    request:  Request,
):
    body = await request.body()
    body_str = body.decode("utf-8")
    try:
        body_dict = json.loads(body_str)
        return {
            "parsed_data": body_dict,
        }
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON format",
        }
        


@app.post("/single/{item_id}")
async def single_data(
    item_id: Annotated[
        int, 
        Path(title="The ID of the item to get", ge=0, le=1000
             )
        ],
    q: str | None = None,
):
    results = {"body": q}
    return results


@app.get("/user/{user_id}/")
async def user_detail(
    user_id: Annotated[int, Path(title="The ID of the user to get", ge=0, le=1000)],
):
    user_data = user_service.get_user(user_id=user_id)
    return user_data



@app.post("/user/", response_model=ResponseUserSchema)
async def create_user(
    user: RequestUserSchema
):
    user_data = user_service.create_user(user) 
    return user_data


@app.get("/user/", response_model=List[ResponseUserSchema])
async def list_users():
    user_data = user_service.list_users() 
    return user_data


@app.post("/book/", response_model=ResponseBookSchema)
async def create_book(
  book: RequestBookSchema
):
    book_data = book.model_dump()
    return book



@app.post("/extra_type/")
async def extra_type(extra_type: ExtraTypeRequest):
    data = extra_type.model_dump(exclude=["color"])
    data["color"] = {
        "named" : extra_type.color.as_named(),
        "as_hex": extra_type.color.as_hex(),
        "as_hsl": extra_type.color.as_hsl_tuple()
    }
    return data


@app.post("/raw_form_data/")
async def form_data(
    request: Request,
    ):
    # if mulitple keys wih same name, latter one will be proccessed    
    form_data = await request.form()
    data = FormData(**form_data._dict)
    return data.model_dump()


@app.post("/form-data/")
async def form_data(
    data: FormData
    # name: Annotated[str, Form()], 
    # address: Annotated[str, Form()]
    ):
    return data.model_dump() 



@app.post("/form_and_file/")
async def form_and_file(
    data: FormData,
    file: UploadFile
):
    return {"filename": "data"}



@app.post("/files/")
async def create_file(file: Annotated[UploadFile, File()]):
    
    return {"file_size": file.size}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    max_file_size_bytes = 10  # 10MB in bytes

    if file.size > max_file_size_bytes:
        raise HTTPException(status_code=400, detail="File size is too large")

    save_file(file=file)
    return {"filename": file.filename}


@app.post("/uploadfiles/")
async def create_upload_files(request: Request, files: list[UploadFile]):
    for file in files:
        save_file(file=file)
    return {"filenames": [file.filename for file in files]}



@app.post("/files/")
async def create_file(
    file:  UploadFile,
    name: Annotated[str, Form()],
    token: Annotated[str, Form()],
):
    return {
        "name": name,
        "token": token,
        "file_content_type": file.content_type,
    }



@app.post("/download")
async def download(data: FileName):
    data = data.model_dump()
    file_path = os.path.join(save_path,  data["file_name"])    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File does not exist.")
    return FileResponse(file_path)

