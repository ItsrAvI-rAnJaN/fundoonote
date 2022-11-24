from .utils import JWT
import logging
import json
from urllib import request
from rest_framework import status
from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import APIView
from .serializers import LoginSerializer,RegisterSerializer
from user.tasks import send_user_email_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from django.contrib import messages

logging.basicConfig(filename='user_logs.log', encoding='utf-8', level=logging.DEBUG)

class Login(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }),
        responses={202: 'ACCEPTED', 400: 'BAD REQUEST'})
    def post(self,request):
        """
         for logging of the user
        """
        try:
            user = authenticate(username=request.data('username'), password=request.data('password'))
            if user is not None:
                token = JWT().encode(
                    data={"username": request.data("username"), "email": user.email})
                return Response({'message': 'Login successfully!',"status":202,"data": {"token":token}},
                             status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message': 'Login failed!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)})
class Register(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def post(self,request):
        try:
            serializer = RegisterSerializer(data=request.Post)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token=JWT().encode(data={"user_id":serializer.data.get("id"),"username":serializer.data.get("username")})
            send_user_email_task.delay(token, serializer.data.get("email"))
            return Response({"message": "User registered sucessfully",'status':201,'data':serializer.data},
                             status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)},status=status.HTTP_400_BAD_REQUEST)

class VerifyToken(APIView):
    def get(self, request, token):
        try:
            jwt_decoder = JWT()
            decoded = jwt_decoder.decode(token)
            user = User.objects.get(id=decoded.get("user_id"))
            user.is_verified = True
            user.save()
            return Response({"message": "Token verified"})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                messages.success(request, "Successfully Logged In")
                return redirect("/")
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login')
        else:
            return render(request, 'login.html')
    except Exception as err:
        logging.exception(err)
        return Response({"message": str(err)})

def register(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            location = request.POST['location']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Exist')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name,phone=phone,location=location)
                    messages.success(request,"user created")
                    return redirect('login')

            else:
                messages.info(request, 'password not matching')
                return redirect('register')
            return redirect('/')
        else:
            return render(request, 'register.html')
    except Exception as err:
        logging.exception(err)
        return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


def logout(request):
    auth.logout(request)
    return redirect('/')