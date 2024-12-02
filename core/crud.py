from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Blog


async def get_blogs(db: AsyncSession):
    result = await db.execute(select(Blog))
    return result.scalars().all()

async def get_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    return result.scalar_one_or_none()

async def create_blog(db: AsyncSession, blog_data):
    new_blog = Blog(**blog_data)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def update_blog(db: AsyncSession, blog_id: int, blog_data):
    blog = await get_blog(db, blog_id)
    if blog:
        for key, value in blog_data.items():
            setattr(blog, key, value)
        await db.commit()
        await db.refresh(blog)
    return blog

async def delete_blog(db: AsyncSession, blog_id: int):
    blog = await get_blog(db, blog_id)
    if blog:
        await db.delete(blog)
        await db.commit()
    return blog
