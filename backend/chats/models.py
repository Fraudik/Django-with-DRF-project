from django.db import models
from users.models import User


class ChatEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=1000, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
