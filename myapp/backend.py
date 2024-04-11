from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class UserRedirectBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        return user
