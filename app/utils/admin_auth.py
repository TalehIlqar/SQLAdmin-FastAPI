from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from account.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(username: str, password: str, session: AsyncSession) -> bool:
    query = await session.execute(f"SELECT * FROM users WHERE username = :username", {"username": username})
    user = query.fetchone()
    if user and pwd_context.verify(password, user.password):
        return True
    return False

async def authentication_callback(request: Request, session: AsyncSession) -> bool:
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    return await authenticate_user(username, password, session)

def is_accessible_callback(request: Request) -> bool:
    return request.session.get("user_authenticated", False)
