from fastapi import FastAPI
from .routes.auth import router as auth_router
from .routes.logs import router as logs_router
import uvicorn
from .models import user_models


app = FastAPI()

app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(auth_router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Monitoring API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)