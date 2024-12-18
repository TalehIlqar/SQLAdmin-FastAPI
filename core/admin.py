from sqladmin import ModelView
from sqlalchemy.future import select

from core.models import Blog



class BlogAdmin(ModelView, model=Blog):
    column_list = ["id", "title", "description", "created_at"]

def setup_core_admin(admin):
    """
    Core tətbiqi üçün admin modellərini qeydiyyatdan keçirmək üçün funksiya.
    """
    admin.add_view(BlogAdmin)
