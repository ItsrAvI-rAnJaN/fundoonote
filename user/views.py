from .utils import JWT
import logging
import json
from urllib import request
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import LoginSerializer,RegisterSerializer


class Login(APIView):
    def post(self,request):
        """
         for logging of the user
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None:
                token = JWT().encode(
                    data={"username": serializer.data.get("username"), "email": serializer.data.get("email")})
                return Response({'message': 'Login successfully!','data':[token]})
            else:
                return Response({'message': 'Login failed!'})

        except Exception as err:
            # print(err)
            logging.exception(err)
            return Response({"message": str(err)})


class Register(APIView):
    def post(self,request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token=JWT().encode(data={"username":serializer.data.get("username"),"email":serializer.data.get("email")})
            print (token)
            return Response({"message": "User registered sucessfully",'status':201,'data':serializer.data},status=status.HTTP_201_CREATED)
        except Exception as err:
            # print(err)
            logging.exception(err)
            return Response({"message": str(err)})