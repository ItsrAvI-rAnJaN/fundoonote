import logging

import jwt
from django.conf import settings
from .models import User


class JWT:
    def encode(self, data):
        if not isinstance(data, dict):
            raise Exception(data, settings.JWT_KEY, algorithm="HS256")

    def decode(self, token):
        try:
            return jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
        except jwt.exceptions.pyJWTError as err:
            raise err

def get_user(request):
    token=request.headers.get("Token")
    decoded=JWT().decode(token)
    if not token:
        raise  Exception ("Token Authentication required")
    user=User.objects.get(username=decoded.get("username"))
    if not user:
        raise Exception("Invalid user")
    if not user.is_verified:
        raise Exception ("user not verified")
    return decoded, user

def verify_user_token(function):

    def wrapper(self, request, *args, **kwargs):
        try:
            payload, user = get_user(request)
            request.data.update({"username" : payload.get("username")})
        except Exception as err:
            logging.exception(err)
        return function(self, request, *args, **kwargs)
    return wrapper

def verify_super_user_token(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            payload, user = get_user(request)
            if not user.is_superuser:
                raise Exception("unauthorized user")
        except Exception as err:
            logging.exception(err)
            return function(self, request, *args, **kwargs)
        return wrapper

