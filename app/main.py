from typing import Union
from app.routes import users
from fastapi import FastAPI
from app import  models
from app.core import database

app = FastAPI()

# Create tables if they do not exist (usually run this once at the beginning)
models.Base.metadata.create_all(bind=database.engine)

app.include_router(users.router,prefix="/api/v1/users", tags=["Users"])

