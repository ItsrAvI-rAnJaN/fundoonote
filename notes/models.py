from django.db import models
from user.models import User


class Labels(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notes(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    collaborator = models.ManyToManyField(User, related_name="notes_collaborator")
    labels = models.ManyToManyField(Labels, related_name="notes_labels")
