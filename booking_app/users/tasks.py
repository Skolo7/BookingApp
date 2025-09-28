from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_password_reset_email(user_email, reset_url):
    """
    Sends password reset email with link.
    """
    subject = 'Reset your password'
    html_message = render_to_string('users/password_reset_confirm.html', {
        'reset_url': reset_url
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject, 
        plain_message,
        from_email, 
        [user_email],
        html_message=html_message,
        fail_silently=False
    )
    return f"Password reset email sent to {user_email}"