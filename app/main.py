from fastapi import FastAPI
from app.api import auth, assets
from app.db.init import *
from app.models import user, asset
import os, uvicorn

try:
    if os.getenv("DEBUG", "false").lower() == "true":
        import debugpy
        print("🚀 Debugger is waiting on port 5678...")
        debugpy.listen(("0.0.0.0", 5678))
except:
    print("😥 Could not attach debugger...")

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}  # Ensure you return a valid response