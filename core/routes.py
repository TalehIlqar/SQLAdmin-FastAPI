from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from core.schemas import BlogRead, BlogCreate
from core.crud import get_blogs, get_blog, create_blog, update_blog, delete_blog

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/", response_model=list[BlogRead])
async def read_blogs(db: AsyncSession = Depends(get_db)):
    return await get_blogs(db)

@router.get("/{blog_id}", response_model=BlogRead)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.post("/", response_model=BlogRead)
async def create_blog_api(blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    return await create_blog(db, blog.dict())

@router.put("/{blog_id}", response_model=BlogRead)
async def update_blog_api(blog_id: int, blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    updated_blog = await update_blog(db, blog_id, blog.dict())
    if not updated_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog

@router.delete("/{blog_id}", response_model=dict)
async def delete_blog_api(blog_id: int, db: AsyncSession = Depends(get_db)):
    deleted_blog = await delete_blog(db, blog_id)
    if not deleted_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
