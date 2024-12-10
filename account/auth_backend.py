
# from fastapi import Request
from starlette.requests import Request
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

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        """
        Admin panel login prosesini idarə edir.
        """
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user and user.is_superuser and verify_password(password, user.password):
                # Tokenlər yaradılır
                access_token = jwt.encode(
                    {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=30)},
                    self.secret_key,
                    algorithm=ALGORITHM,
                )
                refresh_token = jwt.encode(
                    {"sub": username, "exp": datetime.utcnow() + timedelta(days=7)},
                    self.secret_key,
                    algorithm=ALGORITHM,
                )

                # Cookie-lərə tokenlər yazılır
                # response = RedirectResponse(url="/admin", status_code=302)
                request.session.update(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                )
                return True
                # response.set_cookie(key="access_token", value=access_token, httponly=True)
                # response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
                # print(f"Login successful for user: {username}")
                # return response
            
            print("Invalid login credentials")
        return False
    
    async def logout(self, request: Request) -> bool:
        # request.cookies.pop("access_token", None)
        # request.cookies.clear()
        try:
            request.session.clear()
            return True
        except Exception as e:
            print(f"Error during logout: {e}")
            return False

    async def authenticate(self, request: Request) -> bool:
        """
        Tokenləri yoxlayır və refresh token ilə yeniləyir.
        """
        # access_token = request.cookies.get("access_token")
        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")
        # refresh_token = request.cookies.get("refresh_token")

        if not access_token:
            print("Access token not found")
            return False
        
        try:
            # Access token-i yoxlayırıq
            payload = jwt.decode(access_token, self.secret_key, algorithms=[ALGORITHM])
            username = payload.get("sub")

            async with async_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

                if user and user.is_superuser:
                    return True
        except jwt.ExpiredSignatureError:
            # Əgər access token expired olubsa, refresh token istifadə edirik
            print("Access token expired. Trying to use refresh token...")
            if not refresh_token:
                print("Refresh token not found")
                return False
            try:
                payload = jwt.decode(refresh_token, self.secret_key, algorithms=[ALGORITHM])
                username = payload.get("sub")

                async with async_session() as session:
                    query = select(User).where(User.username == username)
                    result = await session.execute(query)
                    user = result.scalar_one_or_none()

                    if user and user.is_superuser:
                        # Yeni access token yaradılır
                        new_access_token = jwt.encode(
                            {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=30)},
                            self.secret_key,
                            algorithm=ALGORITHM,
                        )
                        request.session.update(
                            {
                                "access_token": new_access_token,
                            }
                        )
                        # response = RedirectResponse(url=request.url.path)
                        # response.set_cookie("access_token", new_access_token, httponly=True)
                        # print("Access token refreshed successfully.")
                        return True
            except jwt.ExpiredSignatureError:
                print("Refresh token expired.")
            except JWTError as e:
                print(f"JWTError during refresh: {e}")
        
        return False
