import logging

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

    @verify_user_token
    def get(self, request):
        try:
            note_list = Notes.objects.filter(user=request.data.get("user"))
            serializer = NoteSerializer(note_list, many=True)
            return Response({"message": "Data retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

    @verify_user_token
    def delete(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get("id"))
            note_object.delete()
            return Response({"message": "Note deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
