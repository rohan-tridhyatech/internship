# myapp/urls.py
from django.urls import path
from .views import CustomUserAPIView

urlpatterns = [
    path('users/', CustomUserAPIView.as_view(), name='custom-user-api'),
]
