from fastapi import HTTPException

from routers.auth import router


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=400, detail="Item ID must be greater than 0")
    return {"item_id": item_id}
