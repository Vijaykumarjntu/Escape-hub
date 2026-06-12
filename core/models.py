from django.db import models
from django.contrib.auth.models import User


class WaitingUser(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Waiting: {self.session_id}"


class Room(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    user1_session = models.CharField(max_length=100)
    user2_session = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_id


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    session_id = models.CharField(max_length=100)  # who sent the message
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id}: {self.message[:30]}"