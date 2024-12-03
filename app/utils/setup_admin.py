from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from core.admin import setup_core_admin  
# from account.admin import setup_account_admin  # Əgər əlavə modellər varsa

def setup_admin_models(app: FastAPI):
    """
    Bütün modelləri admin paneldə qeydiyyatdan keçirmək üçün funksiya.
    """
    admin = Admin(app=app, engine=engine, templates_dir="templates")

    # Core modellərini qeydiyyatdan keçirin
    setup_core_admin(admin)

    # Account modellərini qeydiyyatdan keçirin (əgər varsa)
    # setup_account_admin(admin)
