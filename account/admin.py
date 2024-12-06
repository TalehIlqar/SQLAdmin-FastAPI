from sqladmin import ModelView
from account.models import User, Group

# User modeli üçün admin panel görünüşü
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active, User.is_staff, User.is_superuser]
    column_labels = {
        "id": "ID",
        "username": "İstifadəçi Adı",
        "email": "E-poçt",
        "is_active": "Aktivdir",
        "is_staff": "İşçi",
        "is_superuser": "Superuser"
    }
    form_excluded_columns = ["password"]  # Şifrə admin paneldə göstərilməyəcək
    page_size = 10

# Group modeli üçün admin panel görünüşü
class GroupAdmin(ModelView, model=Group):
    column_list = [Group.id, Group.name]
    column_labels = {
        "id": "ID",
        "name": "Qrup Adı",
    }

def setup_account_admin(admin):
    """
    Account tətbiqi üçün admin modellərini qeydiyyatdan keçirmək üçün funksiya.
    """
    admin.add_view(UserAdmin)
    admin.add_view(GroupAdmin)
