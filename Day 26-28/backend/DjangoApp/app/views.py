from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer
from .models import CustomUser
from .utility_func import registration_send_otp_email, login_send_otp_email


class RegisterUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)  # Save user as inactive
            user.generate_otp()
            registration_send_otp_email(user)
            return Response({'detail': 'OTP sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = CustomUser.objects.filter(email=email).first()
        
        if user and user.otp == otp and user.otp_expiration > now():
            user.generate_otp()
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

class UsernamePasswordLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username:
            user = CustomUser.objects.filter(username=username).first()
            if user and user.check_password(password):
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                return Response({'detail': 'Account not active. Please verify your email.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

class EmailLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            user.generate_otp()  
            login_send_otp_email(user)
            return Response({'detail': 'OTP sent to your email for verification.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = CustomUser.objects.filter(email=email).first()

        if user and user.otp == otp and user.otp_expiration > now():
            user.generate_otp()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
