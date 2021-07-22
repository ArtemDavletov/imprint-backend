from django.urls import path
from folder.views import (
    FolderCreateView,
    ShareFolderPermissionView,
    add_folder_view,
    folder_view,
)

urlpatterns = [
    path(r"<str:folder_uuid>", folder_view, name="get folder"),  # GET get folder
    # path(r"<str:folder_uuid>/", update_folder, name="update folder"),  # PUT update folder
    path(r"", FolderCreateView.as_view(), name="create folder"),  # POST create folder
    path(
        r"share/<str:folder_uuid>",
        ShareFolderPermissionView.as_view(),
        name="share folder",
    ),  # GET create shared token
    path(
        r"add/<str:shared_token>", add_folder_view, name="add shared folder"
    ),  # GET, redirect to Application
    # path(r"add/<str:shared_token>", name="add shared folder"),  # POST add folder to user
]
