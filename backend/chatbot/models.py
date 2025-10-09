from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    timestamp = models.DateTimeField(default=timezone.now)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id} for user {self.user_id}"
