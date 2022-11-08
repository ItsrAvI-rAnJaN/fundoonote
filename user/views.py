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
            user = User.objects.filter(username=data.get('username'), password=data.get('password')).first()
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
        data= json.loads(request.body)
        if request.method == 'POST':
            User.objects.create(username=data.get('username'),password=data.get('password'),email=data.get('email'))
            return JsonResponse({"message" : "User registered sucessfully"})
        else:
            return JsonResponse({"message":"Invalid Credential"})

    except Exception as err:
            print(err)
            logging.exception(err)
            return JsonResponse({"message": str(err)})

