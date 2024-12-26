from django.core.mail import send_mail
from django.conf import settings

def registration_send_otp_email(user):
    subject = f'Hello {user.username}, Your OTP for Email Verification'
    message = f'Dear {user.username},\n\nYour OTP is {user.otp}. It will expire in 10 minutes.\n\nThank you for verifying your email.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    
def login_send_otp_email(user):
    subject = f'Hello {user.username}, Your OTP for Login Verification'
    message = f'Dear {user.username},\n\nYour OTP is {user.otp}. It will expire in 10 minutes.\n\nPlease use this OTP to login securely.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
