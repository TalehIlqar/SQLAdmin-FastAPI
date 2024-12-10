import asyncio
from sqlalchemy.future import select
from account.models import User
from app.utils.password_utils import hash_password
from app.database import async_session

async def reset_superuser_password(username: str, new_password: str):
    async with async_session() as session:
        # Superuserin olub olmadığını yoxlayırıq
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        user.is_superuser = True
        await session.commit()
        if not user or not user.is_superuser:
            print(f"No superuser found with the username: {username}")
            return
        print(f"Superuser {username} found!")
        # Yeni parolu hash edib, istifadəçinin parolunu dəyişirik
        user.password = hash_password(new_password)

        # Dəyişiklikləri bazada saxlayırıq
        session.add(user)
        await session.commit()

        print(f"Password for superuser {username} has been reset successfully!")

if __name__ == "__main__":
    # Reset etmək istədiyiniz superuserin adını və yeni şifrəsini daxil edin
    username = "admin"  # Superuserin adı
    new_password = "admin"  # Yeni şifrə


    # Parolu sıfırlamaq üçün funksiyanı işə salırıq
    asyncio.run(reset_superuser_password(username, new_password))
