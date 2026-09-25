from django.contrib import admin
from django.urls import path

from LittleLemonAPI.views import RegistrationView


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/users",
        RegistrationView.as_view({"post": "create"}),
        name="register",
    ),
]