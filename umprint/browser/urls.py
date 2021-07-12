from django.urls import path

from browser.views import CreateBrowserInstance, AddBrowserInstance

urlpatterns = [
    path(r'create/', CreateBrowserInstance.as_view(), name='create_browser'),
    path(r'add/', AddBrowserInstance.as_view(), name='create_browser'),
]
