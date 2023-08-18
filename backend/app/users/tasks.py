from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(to_email, otp):
    subject = "Login OTP"
    message = f"Your One Time Password: {otp}. \n" \
              f"It's expiration time: {settings.OTP_EXPIRATION_IN_MINUTES} minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    send_mail(subject, message, from_email, recipient_list)
