from django.urls import path
from user.views import user_view

urlpatterns = [
    # path(r"", create_user, name="create_user"),
    path(r"<str:user_id>", user_view, name="")
]
