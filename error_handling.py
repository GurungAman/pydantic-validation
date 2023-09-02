from fastapi import HTTPException

from routers.auth import router

# from fastapi.responses import JSONResponse


# @router.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.detail}
#     )


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=400, detail="Item ID must be greater than 0")
    return {"item_id": item_id}
