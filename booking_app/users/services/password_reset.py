import redis
import uuid
from django.conf import settings
from datetime import timedelta
import json
from django.contrib.auth import get_user_model
from users.tasks import send_password_reset_email
from django.urls import reverse

# Redis connection
redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

# Token expiration time (in seconds)
TOKEN_EXPIRY = 24 * 60 * 60  # 24 hours

User = get_user_model()


def generate_password_reset_token(user_email):
    """
    Generates password reset token and stores it in Redis.
    Returns the generated token.
    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return None
    
    token = str(uuid.uuid4())
    
    token_data = {
        'user_id': user.id,
        'email': user.email
    }
    redis_client.setex(
        f"password_reset:{token}",
        TOKEN_EXPIRY,
        json.dumps(token_data)
    )
    
    return token


def validate_password_reset_token(token):
    """
    Validates password reset token.
    Returns user data if token is valid, otherwise None.
    """
    token_key = f"password_reset:{token}"
    token_data = redis_client.get(token_key)
    
    if not token_data:
        return None
    
    try:
        user_data = json.loads(token_data)
        return user_data
    except json.JSONDecodeError:
        return None


def invalidate_password_reset_token(token):
    """
    Invalidates password reset token.
    """
    token_key = f"password_reset:{token}"
    redis_client.delete(token_key)


def send_password_reset_link(request, user_email):
    """
    Generates password reset token and sends email with link.
    """
    token = generate_password_reset_token(user_email)
    if not token:
        return False
    
    reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm_custom', kwargs={'token': token})
    )
    
    send_password_reset_email.delay(user_email, reset_url)
    
    return True