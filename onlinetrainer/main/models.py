from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"EmailConfirmation({self.user.username})"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Текст відгуку", max_length=1000)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    def __str__(self):
        return f"Відгук від {self.user.username} ({self.created_at.strftime('%Y-%m-%d')})"
