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
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                token = JWT().encode(
                    data={"username": request.data.get("username"), "email": user.email})
                return Response({'message': 'Login successfully!',"data": {"token":token}},
                            status=status.HTTP_202_ACCEPTED)
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
            token=JWT().encode(data={"user_id":serializer.data.get("user_id"),"username":serializer.data.get("username")})
            send_mail(
                subject='PyJWT',
                message=settings.BASE_URL + reverse('verify_token_api', kwargs={"token": token}),
                from_email=None,
                recipient_list=[serializer.data.get("email")]
            )
            return Response({"message": "User registered sucessfully",'status':201,'data':serializer.data},status=status.HTTP_201_CREATED)
        except Exception as err:
            # print(err)
            logging.exception(err)
            return Response({"message": str(err)})

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
