from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.setup_admin import setup_admin_models  # setup_admin.py faylından funksiyanı idxal edin
from app.database import engine
from app.middleware import AuthenticationMiddleware
from core.routes import router as blog_router
from core.models import Blog
from account.routes import auth_router

app = FastAPI()

app.add_middleware(AuthenticationMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    # Cədvəlləri yaradın
    async with engine.begin() as conn:
        await conn.run_sync(Blog.metadata.create_all)
    
    # Admin modellərini qeydiyyatdan keçirin
    setup_admin_models(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Admin Panel"}

app.include_router(blog_router, prefix="/api", tags=["Blogs"])
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
