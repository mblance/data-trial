from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=60, unique=True)
    password_hash = models.CharField(max_length=255)

    timestamp = models.DateTimeField()

    def __str__(self):
        return self.username


class Message(models.Model):
    text = models.TextField()
    author_id = models.CharField(max_length=60)

    timestamp = models.DateTimeField()

    def __str__(self):
        return self.author_id