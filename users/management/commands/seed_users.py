from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

DEFAULTS = [
    ("admin", "admin@example.com", "Admin123!", Profile.Role.ADMIN),
    ("agro", "agro@example.com", "Agro123!", Profile.Role.AGRONOMIST),
    ("trader", "trader@example.com", "Trader123!", Profile.Role.TRADER),
    ("farmer", "farmer@example.com", "Farmer123!", Profile.Role.FARMER),
]

class Command(BaseCommand):
    help = "Seed demo users with roles"

    def handle(self, *args, **kwargs):
        for username, email, pw, role in DEFAULTS:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email})
            if created:
                user.set_password(pw)
                user.is_active = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {username}/{pw}"))
            user.profile.role = role
            user.profile.save()
        self.stdout.write(self.style.SUCCESS("Seeding done."))
