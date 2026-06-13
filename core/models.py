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

# Add to existing models
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # GitHub verification (entry ticket)
    github_username = models.CharField(max_length=100, blank=True)
    github_verified = models.BooleanField(default=False)
    github_join_date = models.DateTimeField(null=True, blank=True)
    
    # Real self (this is the gold)
    inner_self = models.TextField(blank=True, help_text="What's actually going on inside?")
    
    struggles = models.TextField(blank=True, help_text="What's hard? What do you hide?")
    
    crazy_interests = models.TextField(blank=True, help_text="What do you love that others don't get?")
    
    what_i_hide = models.TextField(blank=True, help_text="What don't people know about you?")
    
    looking_for = models.TextField(blank=True, help_text="What kind of human do you want to find?")
    
    # Optional extras
    show_github_on_profile = models.BooleanField(default=False)
    allow_anonymous_matching = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s real self"
    
    def is_complete(self):
        """Check if they've filled their real self"""
        return all([
            self.inner_self,
            self.struggles,
            self.crazy_interests,
            self.looking_for
        ])