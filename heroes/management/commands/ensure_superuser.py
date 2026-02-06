import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a Django superuser from env vars if it doesn't already exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("Superuser env vars not set. Skipping.")
            return

        User = get_user_model()

        # Prefer username check, fallback to email if username not on model
        user = None
        if hasattr(User, "USERNAME_FIELD"):
            field = User.USERNAME_FIELD
            lookup_val = username if field == "username" else (email or username)
            user = User.objects.filter(**{field: lookup_val}).first()

        if user:
            # Ensure it's actually superuser/staff
            changed = False
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if changed:
                user.save()
                self.stdout.write("Existing user promoted to superuser.")
            else:
                self.stdout.write("Superuser already exists.")
            return

        # Create new superuser
        try:
            User.objects.create_superuser(username=username, email=email or "", password=password)
            self.stdout.write("Superuser created.")
        except TypeError:
            # If custom user model doesn't take username/email like this
            self.stderr.write("Could not create superuser: user model signature differs.")
