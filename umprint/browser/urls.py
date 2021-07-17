from browser.views import (CreateBrowserInstance, GetAllBrowserInstance,
                           GetBrowserInstance, UpdateBrowserInstance,
                           move_browser_instance)
from django.urls import path

urlpatterns = [
    path(r"<str:browser_uuid>", GetBrowserInstance.as_view(), name="get browser"),
    path(
        r"update/<str:browser_uuid>",
        UpdateBrowserInstance.as_view(),
        name="update browser",
    ),
    path(r"", CreateBrowserInstance.as_view(), name="create browser"),
    path(r"all/", GetAllBrowserInstance.as_view(), name="all browsers for user"),
    path(
        r"move/<str:browser_uuid>/<str:folder_uuid>",
        move_browser_instance,
        name="move browser to another folder",
    ),
]
