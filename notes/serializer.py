import labels as labels
from rest_framework import serializers
from notes.models import Notes
from notes.models import Labels


class NoteSerializer(serializers.ModelSerializer):
    """
    Creates a new `Note`
    """

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user', 'collaborator', "labels"]
        read_only_fields = ['collaborator', "labels"]


class LabelSerializer(serializers.ModelSerializer):
    """
    Creates a new `Note`
    """

    class Meta:
        model = Labels
        fields = ['id', 'title', 'color', 'user', ]
