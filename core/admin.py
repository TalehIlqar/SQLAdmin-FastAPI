from sqladmin import ModelView
from core.models import Blog

class BlogAdmin(ModelView, model=Blog):
    """
    Blog modelini admin paneldə idarə etmək üçün.
    """
    column_list = [Blog.id, Blog.title, Blog.description, Blog.created_at]
    column_labels = {
        "id": "ID",
        "title": "Başlıq",
        "description": "Təsvir",
        "created_at": "Yaradılma Tarixi"
    }
    column_searchable_list = ["title", "description"]
    form_widget_args = {
        "created_at": {"readonly": True},
    }
    page_size = 10

    async def on_model_change(self, data, model, is_created):
        if len(data["title"]) < 5:
            raise ValueError("Başlıq ən azı 5 simvol olmalıdır.")
        return super().on_model_change(data, model, is_created)

def setup_core_admin(admin):
    """
    Core tətbiqi üçün admin modellərini qeydiyyatdan keçirmək üçün funksiya.
    """
    admin.add_view(BlogAdmin)
