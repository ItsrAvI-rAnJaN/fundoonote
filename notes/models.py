from django.db import models
from user.models import User


class Notes(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

