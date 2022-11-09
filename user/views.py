import logging
import json
from django.shortcuts import render
from django.http.response import JsonResponse
from user.models import User
from django.contrib.auth import authenticate


def loginapi(request):
    """
    method: used for login authentication.
    param:username and password.
    return:login is successfull or not.
    """
    try:
        data = json.loads(request.body)
        if request.method == 'POST':
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                return JsonResponse({'message': 'Login successfully!'})
            else:
                return JsonResponse({'message': 'Login failed!'})
    except Exception as err:
        print(err)
        logging.exception(err)
        return JsonResponse({"message": str(err)})


def registration(request):
    """
    method : To registerd user
    """
    try:
        data = json.loads(request.body)
        if request.method == 'POST':
            user = User.objects.create_user(first_name=data.get('first_name'), last_name=data.get('last_name'),
                                            username=data.get('username'), password=data.get('password'),
                                            email=data.get('email'), phone=data.get('phone'),
                                            location=data.get('location'))
            return JsonResponse({"message": "User registered sucessfully"})
        else:
            return JsonResponse({"message": "Invalid Credential"})

    except Exception as err:
        print(err)
        logging.exception(err)
        return JsonResponse({"message": str(err)})
