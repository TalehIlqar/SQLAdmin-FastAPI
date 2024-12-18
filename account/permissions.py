from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Permission


async def create_default_permissions(session: AsyncSession, model_name: str):
    """
    Hər model üçün add, change, delete və view permissions yaradır (asynchronous).
    """
    permissions = [
        {"name": f"Can add {model_name}", "codename": f"add_{model_name}"},
        {"name": f"Can change {model_name}", "codename": f"change_{model_name}"},
        {"name": f"Can delete {model_name}", "codename": f"delete_{model_name}"},
        {"name": f"Can view {model_name}", "codename": f"view_{model_name}"},
    ]
    for perm in permissions:
        result = await session.execute(
            select(Permission).filter_by(codename=perm["codename"])
        )
        existing = result.scalar_one_or_none()
        if not existing:
            new_perm = Permission(name=perm["name"], codename=perm["codename"])
            session.add(new_perm)
    await session.commit()
