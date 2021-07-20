from auth.views import AuthTokenObtainPairView, RegisterApi
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", AuthTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("registration/", RegisterApi.as_view(), name="registration"),
]
