from django.db import models
from rest_framework import serializers


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


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField()


class UserSerializer(ProjectSerializer):

    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(ProjectSerializer):

    class Meta:
        model = Message
        fields = '__all__'
