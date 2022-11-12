from rest_framework import serializers
from notes.models import Notes


class NoteSerializer(serializers.ModelSerializer):
    """
    Creates a new `Note`
    """
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user']