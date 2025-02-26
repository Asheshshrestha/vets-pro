from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import session
from app.utils import router_utils
from app.exceptions.custom_exception import register_exception
from app.config.logger import logger
app = FastAPI(title="Vetspro API",version="1")

origins = [
    "http://localhost",
    "http://localhost:8000"
]

logger.info(f"Allowed origins:{origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed hosts
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



router_utils.include_routers(app)



@app.get("/")
def read_root():
    return {"message": "App is running"}

register_exception(app)