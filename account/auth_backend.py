from app.utils.password_utils import verify_password
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError
from account.models import User
from app.database import async_session
from sqlalchemy.future import select

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)  # secret_key arqumentini göndərin
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with async_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            print('user.password', user.password)
            print('password', password)
            password_is_okay = verify_password(password, user.password)
            print('password_is_okay', password_is_okay)
            if user and user.is_superuser and password_is_okay:  # Şifrə yoxlanır
                print("User is authenticated ================================================")
                token = jwt.encode({"sub": username}, self.secret_key, algorithm=ALGORITHM)
                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie("access_token", token, httponly=True)
                return response
        return False

    async def logout(self, request: Request) -> bool:
        response = RedirectResponse(url="/login", status_code=302)
        response.delete_cookie("access_token")
        return response

    async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("access_token")
        if not token:
            return False
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return False

            async with async_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

                if user and user.is_superuser:
                    return True
        except JWTError:
            return False
        return False
