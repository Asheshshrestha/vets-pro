from fastapi import FastAPI
from app.api.v1 import (user_router,
                        token_router)

def include_routers(app:FastAPI):
    app.include_router(user_router)
    app.include_router(token_router)