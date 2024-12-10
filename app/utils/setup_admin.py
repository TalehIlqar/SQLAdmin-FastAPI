from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from core.admin import setup_core_admin
from account.admin import setup_account_admin
from account.auth_backend import AdminAuthBackend  # Auth backend faylından idxal edin

def setup_admin_models(app: FastAPI):
    """
    Bütün modelləri admin paneldə qeydiyyatdan keçirmək üçün funksiya.
    """
    auth_backend = AdminAuthBackend(secret_key="your-secret-key")  # Auth backend yaradın

    admin = Admin(
        title="Hyundai Admin Panel",
        app=app,
        engine=engine,
        authentication_backend=auth_backend,  # Admin auth backend əlavə edin
        templates_dir="templates"  # Şablonlar üçün qovluq
    )

    # Core modellərini qeydiyyatdan keçirin
    setup_core_admin(admin)
    setup_account_admin(admin)
