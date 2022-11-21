from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.BigIntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        db_table = "user"


class UserLogs(models.Model):
    method = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
