from rest_framework import serializers
from notes.models import Notes
from drf_yasg import openapi


class NoteSerializer(serializers.ModelSerializer):
    """
    Creates a new `Note`
    """

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user']
        swagger_schema_fields = {"required": ["tittle", "description"], "type": openapi.TYPE_OBJECT}
