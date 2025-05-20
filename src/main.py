from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from utils.error.exception_handler import register_exception_handlers
from src.routers import health_check
from src.routers.nas import create, move, delete, rename
from src.secret import MIDDLEWARE_SECRET_KEY


app = FastAPI(
    root_path="/api/v1/nas",
    title="NAS-CRUD",
    description="Backend service to integrate ERP with internal NAS.",
    version="1.0.0",
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(middleware_class=SessionMiddleware, secret_key=MIDDLEWARE_SECRET_KEY)
app.include_router(health_check.router)
app.include_router(create.router)
app.include_router(move.router)
app.include_router(delete.router)
app.include_router(rename.router)
