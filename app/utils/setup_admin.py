from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from core.admin import setup_core_admin
from account.admin import setup_account_admin
from account.auth_backend import AdminAuthBackend 
# from app.settings import SECRET_KEY
SECRET_KEY = "your-secret-key"

def setup_admin_models(app: FastAPI):
    """
    Bütün modelləri admin paneldə qeydiyyatdan keçirmək üçün funksiya.
    """
    auth_backend = AdminAuthBackend(secret_key=SECRET_KEY)

    admin = Admin(
        title="Hyundai Admin Panel",
        app=app,
        engine=engine,
        authentication_backend=auth_backend, 
        templates_dir="templates"  
    )

    # Core modellərini qeydiyyatdan keçirin
    setup_core_admin(admin)
    setup_account_admin(admin)
