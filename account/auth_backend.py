from app.utils.password_utils import verify_password
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError
from sqlalchemy.future import select
from datetime import datetime, timedelta

from account.models import User
from app.database import async_session

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user and user.is_superuser and verify_password(password, user.password):
                token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}, self.secret_key, algorithm=ALGORITHM)
                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie("access_token", token, httponly=True)
                return response
        return False

    async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("access_token")
        if not token:
            print("Token not found")
            return False
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                print("Username not found in token")
                return False
            
            async with async_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()
                if user and user.is_superuser:
                    return True
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except JWTError as e:
            print(f"JWT Error: {e}")
        return False
