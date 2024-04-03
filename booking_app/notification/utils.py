from django.conf import settings
from django.core.mail import send_mail


def send_mail_to_client():
    subject = ""
    message = ""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = []

    send_mail()
