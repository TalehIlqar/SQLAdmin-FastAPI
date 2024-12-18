
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from jose import jwt, JWTError
from sqlalchemy.future import select
from datetime import datetime, timedelta
from account.models import User
from app.database import async_session
from account.utils.password_utils import verify_password
# from app.settings import ALGORITHM
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
            
            if user and (user.is_superuser or user.is_staff) and verify_password(password, user.password):
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

                request.session.update(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user_id": user.id,
                    }
                )
                return True
            
        return False
    
    async def logout(self, request: Request) -> bool:
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
        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")

        if not access_token:
            return False
        
        try:
            # Access token-i yoxlayırıq
            payload = jwt.decode(access_token, self.secret_key, algorithms=[ALGORITHM])
            username = payload.get("sub")

            async with async_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalar_one_or_none()

                if user and (user.is_superuser or user.is_staff):

                    return True
                
        except jwt.ExpiredSignatureError:
            if not refresh_token:
                return False
            try:
                payload = jwt.decode(refresh_token, self.secret_key, algorithms=[ALGORITHM])
                username = payload.get("sub")

                async with async_session() as session:
                    query = select(User).where(User.username == username)
                    result = await session.execute(query)
                    user = result.scalar_one_or_none()

                    if user and (user.is_superuser or user.is_staff):

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
                        return True
            except jwt.ExpiredSignatureError:
                print("Refresh token expired.")
            except JWTError as e:
                print(f"JWTError during refresh: {e}")
        
        return False
