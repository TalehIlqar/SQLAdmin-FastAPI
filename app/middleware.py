from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.future import select
from jose import jwt, JWTError
from account.models import User
from app.database import async_session

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin") and request.url.path != "/admin/login":
            token = request.cookies.get("access_token")
            if not token:
                return RedirectResponse(url="/admin/login")  # `/admin/login`-ə yönləndirmə
        return await call_next(request)

# class AuthenticationMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/admin") and request.url.path != "/login":
#             token = request.cookies.get("access_token")
#             if not token:
#                 return RedirectResponse(url="/login")
#             try:
#                 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#                 username = payload.get("sub")
#                 if username is None:
#                     raise HTTPException(status_code=403, detail="Invalid credentials")
#                 async with async_session() as session:
#                     query = select(User).where(User.username == username)
#                     result = await session.execute(query)
#                     user = result.scalar_one_or_none()
#                     if not user or not user.is_superuser:
#                         raise HTTPException(status_code=403, detail="Permission denied")
#             except JWTError:
#                 return RedirectResponse(url="/login")
#         return await call_next(request)
