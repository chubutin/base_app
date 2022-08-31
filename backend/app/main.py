from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.users import user_router, user_router_no_auth_required, login_router
from settings import Settings
from utils.errors import AppException

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

setting = Settings()
app = FastAPI(title=setting.appName)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(user_router_no_auth_required)


@app.get("/status")
async def read_root():
    return {"status": "ok"}


@app.get("/")
async def home():
    return {"hello": "world"}


@app.exception_handler(AppException)
async def unicorn_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={"message": f"{exc}",
                 "request": str(request.url)},
    )
