from sqladmin import ModelView
from core.models import Blog


class BlogAdmin(ModelView, model=Blog):
    """
    Blog modelini admin paneldə idarə etmək üçün.
    """
    column_list = [Blog.id, Blog.title, Blog.description, Blog.created_at]

def setup_core_admin(admin):
    """
    Core tətbiqi üçün admin modellərini qeydiyyatdan keçirmək üçün funksiya.
    """
    admin.add_view(BlogAdmin)
