from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from core.admin import setup_core_admin  # Blog modeli üçün admin qeydiyyatı
# from account.admin import setup_account_admin  # Əgər əlavə modellər varsa

def setup_admin_models(app: FastAPI):
    """
    Bütün modelləri admin paneldə qeydiyyatdan keçirmək üçün funksiya.
    """
    admin = Admin(app=app, engine=engine)

    # Core modellərini qeydiyyatdan keçirin
    setup_core_admin(admin)

    # Account modellərini qeydiyyatdan keçirin (əgər varsa)
    # setup_account_admin(admin)
