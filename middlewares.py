from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("start middleware")
        response = await call_next(request)
        print("end middleware")
        return response
    
async def middleware_one(request: Request, call_next):
    print("middleware 2")
    response = await call_next(request)
    print("end middleware 2")
    return response
