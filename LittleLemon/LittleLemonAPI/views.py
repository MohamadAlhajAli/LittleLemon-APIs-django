from django.shortcuts import render

from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny


class RegistrationView(UserViewSet):
    http_method_names = ["post", "options"]

    def get_permissions(self):
        return [AllowAny()]