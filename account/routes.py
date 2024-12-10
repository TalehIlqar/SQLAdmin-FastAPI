from fastapi import APIRouter, Request, HTTPException, Response, Form
from jose import jwt, JWTError
from datetime import datetime, timedelta
from account.models import User
from app.database import async_session
from sqlalchemy.future import select
from app.utils.password_utils import verify_password
from app.settings import SECRET_KEY, ALGORITHM

auth_router = APIRouter()

@auth_router.post("/login")
async def login(
    username: str = Form(...), 
    password: str = Form(...), 
    response: Response = None
):
    async with async_session() as session:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Access and Refresh token creation
        access_token = jwt.encode(
            {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=30)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        refresh_token = jwt.encode(
            {"sub": username, "exp": datetime.utcnow() + timedelta(days=7)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        # Set cookies
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {"message": "Login successful"}

@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}

@auth_router.post("/refresh")
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        new_access_token = jwt.encode(
            {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=1)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        response = {"access_token": new_access_token}
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
