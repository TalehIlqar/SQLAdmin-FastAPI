# from app.utils.password_utils import verify_password
# from fastapi import Request
# from fastapi.responses import RedirectResponse
# from sqladmin.authentication import AuthenticationBackend
# from jose import jwt, JWTError
# from sqlalchemy.future import select
# from datetime import datetime, timedelta

# from account.models import User
# from app.database import async_session

# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"

# class AdminAuthBackend(AuthenticationBackend):
#     def __init__(self, secret_key: str):
#         super().__init__(secret_key=secret_key)
#         self.secret_key = secret_key

#     async def login(self, request: Request) -> bool:
#         form = await request.form()
#         username = form.get("username")
#         password = form.get("password")

#         async with async_session() as session:
#             query = select(User).where(User.username == username)
#             result = await session.execute(query)
#             user = result.scalar_one_or_none()
#             if user and user.is_superuser and verify_password(password, user.password):
#                 token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}, self.secret_key, algorithm=ALGORITHM)
#                 response = RedirectResponse(url="/admin", status_code=302)
#                 response.set_cookie("access_token", token, httponly=True)
#                 return response
#         return False

#     async def authenticate(self, request: Request) -> bool:
#         token = request.cookies.get("access_token")
#         if not token:
#             print("Token not found")
#             return False
#         try:
#             payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
#             username = payload.get("sub")
#             if username is None:
#                 print("Username not found in token")
#                 return False
            
#             async with async_session() as session:
#                 query = select(User).where(User.username == username)
#                 result = await session.execute(query)
#                 user = result.scalar_one_or_none()
#                 if user and user.is_superuser:
#                     return True
#         except jwt.ExpiredSignatureError:
#             print("Token has expired@@")
#         except JWTError as e:
#             print(f"JWT Error: {e}")
#         return False

from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError
from sqlalchemy.future import select
from datetime import datetime, timedelta

from account.models import User
from app.database import async_session
from app.utils.password_utils import verify_password

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        """İstifadəçini yoxlayır və tokenlər yaradır."""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        print(f"Login attempt: username={username}")

        async with async_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user and user.is_superuser and verify_password(password, user.password):
                access_token = jwt.encode(
                    {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
                    self.secret_key,
                    algorithm=ALGORITHM,
                )
                refresh_token = jwt.encode(
                    {"sub": username, "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)},
                    self.secret_key,
                    algorithm=ALGORITHM,
                )

                print(f"Login successful: username={username}")
                print(f"Access token: {access_token}")
                print(f"Refresh token: {refresh_token}")

                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie("access_token", access_token, httponly=True)
                response.set_cookie("refresh_token", refresh_token, httponly=True)
                return response
            print("Login failed: Invalid credentials")
        return False

    async def logout(self, request: Request) -> bool:
        """İstifadəçini logout edir."""
        print("Logout initiated")
        response = RedirectResponse(url="/admin/login", status_code=302)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        print("Logout successful")
        return response

    async def authenticate(self, request: Request) -> bool:
        """Access tokeni yoxlayır və lazımsa refresh token ilə yenidən yaradır."""
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        print("Authenticating request")

        if not access_token:
            print("Access token not found")
            return False

        try:
            payload = jwt.decode(access_token, self.secret_key, algorithms=[ALGORITHM])
            username = payload.get("sub")
            print(f"Access token valid for username: {username}")

            if username is None:
                print("Username not found in token")
                return False

            async with async_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

                if user and user.is_superuser:
                    print(f"User authenticated: {username}")
                    return True

        except jwt.ExpiredSignatureError:
            print("Access token expired. Attempting to refresh...")

            if not refresh_token:
                print("Refresh token not found")
                return False

            try:
                payload = jwt.decode(refresh_token, self.secret_key, algorithms=[ALGORITHM])
                username = payload.get("sub")

                if username is None:
                    print("Username not found in refresh token")
                    return False

                # Yeni access token yaradır
                new_access_token = jwt.encode(
                    {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
                    self.secret_key,
                    algorithm=ALGORITHM,
                )
                print("Access token refreshed successfully")
                response = RedirectResponse(url=request.url.path)
                response.set_cookie("access_token", new_access_token, httponly=True)
                return True

            except jwt.ExpiredSignatureError:
                print("Refresh token expired")
                return False
            except JWTError as e:
                print(f"Refresh token error: {e}")
                return False

        except JWTError as e:
            print(f"Access token error: {e}")
            return False

        print("Authentication failed")
        return False
