# models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_claimed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
