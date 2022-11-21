import logging

import jwt
from django.conf import settings
from rest_framework.response import Response

from .models import User



class JWT:
    def encode(self, data):
        if not isinstance(data, dict):
            raise Exception("Data is not in dictionary")
        encode_jwt = jwt.encode(data, settings.JWT_KEY, algorithm="HS256")
        return encode_jwt.decode("utf-8")

    def decode(self, token):
        try:
            return jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
        except jwt.exceptions.pyJWTError as err:
            raise err


def verify_user_token(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        if token is None:
            return Response({"message":"Token Authentication required"},status=400)
        payload = JWT().decode(token)
        user = User.objects.get(username=payload.get("username"))
        if not user:
            raise Exception("Invalid user")
        request.data.update({"user": user.id})
        var = function(self, request, *args, **kwargs)
        return var

    return wrapper
