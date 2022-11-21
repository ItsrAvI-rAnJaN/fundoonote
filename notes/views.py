import logging
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from .redish_note import RedisNote
from .serializer import NoteSerializer, LabelSerializer
from user.utils import verify_user_token
from .models import Notes, Labels

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
            created_data = RedisNote().set(serializer.data.get("user"), serializer.data)
            return Response({"message": "Note created Successfully", "redis_data": created_data},
                            status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    @verify_user_token
    def get(self, request):
        try:
            note_list = Notes.objects.filter(user=request.data.get("user"))
            serializer = NoteSerializer(note_list, many=True)
            if not serializer.data:
                raise Exception("Wrong credentials")
            get_data = RedisNote().get(request.data.get("user"))
            return Response({"message": "Data retrieved", "redis_data": get_data}, status=status.HTTP_200_OK)
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
            updated_data = RedisNote().set(request.data.get('user'),serializer.data)
            return Response({"message": "Update successful", "redis_data": updated_data},
                            status=status.HTTP_201_CREATED)
            # return Response({"message": "Update successful", "data": serializer.data},
            #                 status=status.HTTP_201_CREATED)
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
            user_id=request.data.get("user")
            note_id=request.data.get("id")
            note_object = Notes.objects.get(id=request.data.get("id"))
            # note_object.delete()
            RedisNote().delete(user_id,note_id)
            return Response({"message": "Note deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NotesCollaboratorAPI(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'notes_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'collaborator': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_user_token
    def post(self, request):
        try:
            notes_obj = Notes.objects.get(id=request.data.get("notes_id"))
            user_id = request.data.get("collaborator")
            user_object = User.objects.get(id=user_id)
            notes_obj.collaborator.add(user_object)
            return Response({"message": "Collaborator created", "data": {"Collaborator": user_object.id}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'notes_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'collaborator': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_user_token
    def delete(self, request):
        try:
            notes_obj = Notes.objects.get(id=request.data.get("notes_id"))
            user_obj = request.data.get("collaborator")
            notes_obj.collaborator.remove(user_obj)
            return Response({"message": "Collaborator deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LabelsAPI(APIView):
    @swagger_auto_schema(request_body=LabelSerializer,
                         responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_user_token
    def post(self, request):
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label created", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    @verify_user_token
    def get(self, request):
        try:
            note_list = Labels.objects.filter(user=request.data.get("user"))
            serializer = LabelSerializer(note_list, many=True)
            return Response({"message": "Data retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'labels_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'color': openapi.Schema(type=openapi.TYPE_STRING)
        }), responses={201: 'CREATED', 406: 'NOT ACCEPTABLE', 400: 'BAD REQUEST'})
    @verify_user_token
    def put(self, request):
        try:
            note_object = Labels.objects.get(id=request.data.get("labels_id"))
            serializer = LabelSerializer(note_object, data=request.data)
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
            'labels_id': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={200: 'OK', 400: 'BAD REQUEST'})
    @verify_user_token
    def delete(self, request):
        try:
            label_object = Labels.objects.get(id=request.data.get("labels_id"))
            label_object.delete()
            return Response({"message": "Label deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NotesLabelAPI(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'notes_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'label_id': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),
        responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_user_token
    def post(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get("notes_id"))
            labels_object = Labels.objects.get(id=request.data.get("label_id"))
            note_object.labels.add(labels_object)
            return Response({"message": "Label created", "data": {"Label": labels_object.id}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'notes_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'label_id': openapi.Schema(type=openapi.TYPE_INTEGER)
        }),responses={201: 'CREATED', 400: 'BAD REQUEST'})
    @verify_user_token
    def delete(self, request):
        try:
            note_object = Notes.objects.get(id=request.data.get("notes_id"))
            label_object = Labels.objects.get(id=request.data.get("label_id"))
            note_object.labels.remove(label_object)
            return Response({"message": "Label deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
