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
#         # Yalnız admin panel yolları üçün yoxlama
#         if request.url.path.startswith("/admin") and request.url.path != "/admin/login":
#             token = request.cookies.get("access_token")  # Cookie-də tokeni yoxlayırıq
#             if not token:
#                 print("Access token not found. Redirecting to /admin/login")
#                 return RedirectResponse(url="/admin/login")  # Token yoxdursa, yönləndirmə

#             try:
#                 # Token doğrulanır
#                 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#                 username = payload.get("sub")
#                 if not username:
#                     print("Username not found in token. Redirecting to /admin/login")
#                     return RedirectResponse(url="/admin/login")

#                 # İstifadəçinin superuser olub-olmadığını yoxlayırıq
#                 async with async_session() as session:
#                     query = select(User).where(User.username == username)
#                     result = await session.execute(query)
#                     user = result.scalar_one_or_none()

#                     if not user or not user.is_superuser:
#                         print("User is not superuser or does not exist.")
#                         return RedirectResponse(url="/admin/login")

#                     # Əgər hər şey qaydasındadırsa, növbəti middleware və ya endpointə keçid
#                     print(f"Authenticated user: {user.username}")
#             except jwt.ExpiredSignatureError:
#                 print("Access token has expired. Redirecting to /admin/login")
#                 return RedirectResponse(url="/admin/login")
#             except JWTError as e:
#                 print(f"Token error: {e}. Redirecting to /admin/login")
#                 return RedirectResponse(url="/admin/login")

#         # Başqa yollar üçün yoxlama olmadan davam et
#         return await call_next(request)