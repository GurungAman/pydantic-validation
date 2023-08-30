from enum import Enum

from fastapi import FastAPI, Path, Query

app =  FastAPI()

#Path Parameters

@app.get("/")
async def root():
    return {"message":"Let's get started with FastAPI Basics!"}


@app.get("/users")
async def get_user():
    return {"message": "This takes us to the users page."}  

@app.get("/users/{user_id}")
async def get_user(user_id):
    return {"user_id": user_id}         #accepts any type for id

@app.get("/employee/{emp_id}")
async def get_employee(emp_id:int):
    return {"employee_id": emp_id}   

# @app.get("/employee/{emp_id}")
# async def get_user(emp_id:str):
#     return {"employee_id": emp_id}      

@app.get("/employee/rashmi")
async def get_current_employee():
    return {"message": "This is the current employee"}



#Predefined Values (Enum)

class ModelName(str, Enum):
    cow = "cow"
    lion = "lion"
    fish = "fish"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.cow:            #comparing the path parameter(enumeration member)
        return {"model_name": model_name, "message": "Domestic animal"}

    if model_name.value == "lion":           #getting the value
        return {"model_name": model_name, "message": "Wild animal"}

    return {"model_name": model_name, "message": "Aquatic"}       #returning enumeration member


#Query Parameters

items_db = [{"item_name": "Book"}, {"item_name": "Pen"}, {"item_name": "Copy"}]


@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):           #optional parameter
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}



@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an example of query parameter type conversion"}         
        )
    
    return item


#String Validation in Query Params

@app.get("/products/")
async def read_products(q: str = Query(..., min_length=3, max_length=10)):
    return {"q": q}


#Numeric Validation in Path Parameters

@app.get("/students/{student_id}")
async def read_students(student_id: int = Path(..., gt=5, le=10)):
    return {"student_id": student_id}

#Request Body

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_by: str | None = None
    due_date: str

@app.post("/tasks/")
async def create_task(task: TaskCreate):
    
    # Here, "task" is the request body data, automatically validated and converted based on the model.

    # We can use "task.title", "task.description", etc. to access the data.

    # Our code to save the task to a database or perform any other actions goes here.

    return {"message": "Task created successfully"}
