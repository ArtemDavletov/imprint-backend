from django.urls import path

from user.views import create_user, get_user_by_id, update_user

urlpatterns = [
    path(r'create/', create_user, name='create_user'),
    path(r'get/<str:id>/', get_user_by_id, name='get_user_by_id'),
    path(r'update/', update_user, name='update_user'),
]
