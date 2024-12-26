from django.urls import path
from .views import RegisterUserAPIView, VerifyEmailRegistrationAPIView, UsernamePasswordLoginAPIView,EmailLoginAPIView,VerifyEmailLoginAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('verify-otp/', VerifyEmailRegistrationAPIView.as_view(), name='verify-otp'),
    path('username-login/', UsernamePasswordLoginAPIView.as_view(), name='username-login'),
    path('email-login/', EmailLoginAPIView.as_view(), name='email-login'),
    path('verify-email-login/', VerifyEmailLoginAPIView.as_view(), name='verify-email-login'),
]



