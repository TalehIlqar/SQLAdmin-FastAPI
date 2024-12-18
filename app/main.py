from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.setup_admin import setup_admin_models
from app.database import engine
from core.routes import router as blog_router
# from core.models import Blog
from app.database import Base

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    # Cədvəlləri yaradın
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    setup_admin_models(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Admin Panel"}

app.include_router(blog_router, prefix="/api", tags=["Blogs"])