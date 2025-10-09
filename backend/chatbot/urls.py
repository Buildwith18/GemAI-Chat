# chatbot/urls.py
from django.urls import path
from .views import chatbot_reply, health_check, get_chat_history, clear_chat, get_sessions

urlpatterns = [
    path('chat/', chatbot_reply, name='chatbot_reply'),
    path('health/', health_check, name='health_check'),
    path('history/', get_chat_history, name='get_chat_history'),
    path('clear/', clear_chat, name='clear_chat'),
    path('sessions/', get_sessions, name='get_sessions'),
]
