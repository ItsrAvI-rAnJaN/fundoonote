import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import NoteSerializer
from user.utils import verify_user_token
from .models import Notes

logging.basicConfig(filename='user_logs.log', encoding='utf-8', level=logging.DEBUG)


class NoteAPI(APIView):
    """
    Creates a new `Note`
    """

    @swagger_auto_schema(request_body=NoteSerializer,
                         responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_user_token
    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note created Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_user_token
    def get(self, request):
        try:
            note_list = Notes.objects.filter(user=request.data.get("user"))
            serializer = NoteSerializer(note_list, many=True)
            return Response({"message": "Data retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING)
        }),
        responses={201: "ok", 400: "BAD REQUEST"})
    @verify_user_token
    def put(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get("id"))
            serializer = NoteSerializer(note_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Update successful", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_user_token
    def delete(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get("id"))
            note_object.delete()
            return Response({"message": "Note deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
