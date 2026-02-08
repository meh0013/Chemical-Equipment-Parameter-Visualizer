from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
import os


class EquipmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'equipment'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import User
        import os

    def create_demo_user(sender, **kwargs):
        password = os.environ.get("DEMO_PASSWORD", "changeme123")

        user, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        # ALWAYS sync password from env
        user.set_password(password)
        user.save()