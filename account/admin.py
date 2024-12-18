from sqladmin import ModelView
from .models import User, Group, Permission


class UserAdmin(ModelView, model=User):
    column_list = ["id", "username", "email", "is_active", "is_staff", "groups", "user_permissions"]
    form_excluded_columns = ["password"]

    form_args = {
        "groups": {
            "label": "Groups",
            "query_factory": lambda: Group.query.all(),
            "widget": "selectmultiple",
        },
        "user_permissions": {
            "label": "User Permissions",
            "query_factory": lambda: Permission.query.all(),
            "widget": "selectmultiple",
        },
    }


class GroupAdmin(ModelView, model=Group):
    column_list = ["id", "name", "permissions"]
    form_args = {
        "permissions": {
            "label": "Permissions",
            "query_factory": lambda: Permission.query.all(),
            "widget": "selectmultiple",
        },
    }


class PermissionAdmin(ModelView, model=Permission):
    column_list = ["id", "name", "codename"]


def setup_account_admin(admin):
    """
    Account tətbiqi üçün admin modellərini qeydiyyatdan keçirmək üçün funksiya.
    """
    admin.add_view(UserAdmin)
    admin.add_view(PermissionAdmin)

