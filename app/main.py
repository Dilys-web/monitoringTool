from fastapi import FastAPI
from .routes.auth import router as auth_router
import uvicorn
from .models import user_models


app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Monitoring API"}

if __name__ == "__main__":
    uvicorn.run("app,main:app", reload=True)