# from fastapi import Cookie, FastAPI, Header, Response

# app = FastAPI()


# @app.post("/set-cookie/")
# def SetCookie(response: Response):
#     response.set_cookie(key="fakesession", value="fake-cookie-session-value")
#     return {"message": "Fake cookie has been set."}


# @app.get("/get-cookie/")
# def GetCookie(fakesession: str | None = Cookie(None)):
#     return {"fake-cookie": fakesession}


# @app.get("/get-headers/")
# def GetHeader(accept_encoding: str | None = Header(None), sec_ch_ua: str | None = Header(None)):
#     return {
#         "Accept-Encoding": accept_encoding,
#         "Sec-Ch-Ua": sec_ch_ua
#     }


from fastapi import FastAPI

from routers import auth, protected

app = FastAPI()

app.include_router(auth.router)
app.include_router(protected.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
