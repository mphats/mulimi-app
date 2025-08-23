from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        AGRONOMIST = "AGRONOMIST", "Agronomist"
        TRADER = "TRADER", "Trader"
        FARMER = "FARMER", "Farmer"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"



from django.db import models
from django.utils import timezone
import uuid

class MagicLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='magic_links')
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def mark_used(self):
        self.used = True
        self.save()
