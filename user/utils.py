import logging

import jwt
from django.conf import settings
from .models import User


class JWT:
    def encode(self, data):
        if not isinstance(data, dict):
            raise Exception("Data is not in dictionary")
        encode_jwt=jwt.encode(data,settings.JWT_KEY, algorithm="HS256")
        return encode_jwt

    def decode(self, token):
        try:
            return jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
        except jwt.exceptions.pyJWTError as err:
            raise err




def verify_user_token(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        print(token)
        if token is None:
            raise Exception("Token Authentication required")
        payload = JWT().decode(token)
        print(payload)
        user = User.objects.get(username=payload.get("username"))
        if not user:
            raise Exception("Invalid user")
        # if not user.is_verified:
        #     raise Exception("user not verified")
        request.data.update({"user":user.id})
        var = function(self, request, *args, **kwargs)
        return var

    return wrapper
