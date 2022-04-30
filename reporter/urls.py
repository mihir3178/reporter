from django.contrib import admin
from django.urls import path
from auth_app.views import login_api, logout_api
from report_app.views import delete_data, view_uploaded_data, upload_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_api, name="login"),
    path("logout", logout_api, name="logout"),
    path("upload_data", upload_data, name="upload_data"),
    path("", view_uploaded_data, name="view_uploaded_data"),
    path("delete_data", delete_data, name="delete_data"),
]
