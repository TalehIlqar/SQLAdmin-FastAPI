import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from account.models import User
from account.utils.password_utils import hash_password
from app.database import async_session

async def create_or_update_superuser(username: str, email: str, password: str):
    async with async_session() as session:
        async with session.begin(): 
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalars().first()

            if user:
                print(f"Superuser '{username}' already exists. Updating password.")
                user.password = hash_password(password)
                user.email = email
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
            else:
                print(f"Creating new superuser '{username}'.")
                user = User(
                    username=username,
                    email=email,
                    password=hash_password(password),
                    is_superuser=True,
                    is_staff=True,
                    is_active=True
                )
                session.add(user)

        await session.commit()
        print(f"Superuser '{username}' created/updated successfully!")

if __name__ == "__main__":
    username = "talehilgar"
    email = "test@gmail.com"
    password = "admin_password"

    asyncio.run(create_or_update_superuser(username, email, password))
