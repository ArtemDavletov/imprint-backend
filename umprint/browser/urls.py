from django.urls import path

from browser.views import CreateBrowserInstance, GetBrowserInstance, UpdateBrowserInstance

urlpatterns = [
    path(r'<str:browser_uuid>', GetBrowserInstance.as_view(), name='get browser'),
    path(r'update/<str:browser_uuid>', UpdateBrowserInstance.as_view(), name='update browser'),
    path(r'', CreateBrowserInstance.as_view(), name='create browser'),
]
