from django.urls import path
from user.views import UserProfileView

urlpatterns = [
    # path(r"", create_user, name="create_user"),
    path(r"<str:user_id>", UserProfileView.as_view(), name="")
]
