import asyncio
from sqlalchemy.future import select
from account.models import User
from app.utils.password_utils import hash_password
from app.database import async_session

async def create_or_update_superuser(username: str, email: str, password: str):
    """
    Superuser yaradın və ya mövcud superuserin parolunu və xüsusiyyətlərini yeniləyin.
    """
    async with async_session() as session:
        # İstifadəçini tapmaq üçün sorğu
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            print(f"Superuser '{username}' already exists. Updating password and permissions.")
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

        # Dəyişiklikləri saxlayırıq
        await session.commit()
        print(f"Superuser '{username}' created/updated successfully!")

if __name__ == "__main__":
    # Superuser məlumatları
    username = "admin8"  # Superuser adı
    email = "admin8@example.com"  # Superuser email
    password = "strong_password8"  # Superuser şifrəsi

    # Funksiyanı işə salırıq
    asyncio.run(create_or_update_superuser(username, email, password))
