from django.urls import path
from . import views

urlpatterns = [
    path('users', views.user_api),
    path('messages', views.message_api),
]
